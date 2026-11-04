"""Follow two server-selected HTML links with only guest keyboard events."""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from time import monotonic, sleep

from arp_link import GUEST_IP
from guest_tool import Guest
from tcp_peer import HTTP_PORT
from verify_browser_paths import check_screen, read_requests
from verify_shell import read_prompt
from verify_tcp import segments


def wait_page(guest, path, index):
    line = f"GET {path} HTTP/1.0"
    deadline = monotonic() + 6
    while monotonic() < deadline:
        requests = read_requests(guest)
        if len(requests) > index:
            request = requests[index]
            if request["request"] != line:
                raise ValueError(f"Unexpected HTTP request {request['request']!r}, expected {line!r}")
            body = request["body"]
            expected = re.search(r"<h1>([A-Z ]+)</h1><p>([A-Z ]+)</p>", body).groups()
            return body, check_screen(guest, expected)
        sleep(0.05)
    raise ValueError(f"Origin did not receive {line!r}")


def check_link_cue(screenshot, linked):
    pixel = subprocess.check_output([
        "magick", str(screenshot), "-crop", "1x1+146+105", "+repage", "-depth", "8", "rgb:-",
    ])
    expected = bytes.fromhex("00ff00" if linked else "101820")
    if pixel != expected:
        raise ValueError(f"Unexpected link cue at {screenshot}: {pixel.hex()}")


def main():
    root = Path(".local/browser-link-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    guest = Guest(workspace)
    paths = ["/index.html"]
    screenshots = []
    try:
        guest.boot(network=True, http=True, disk=True, display=True, browser=True, paths=True, links=True)
        read_prompt(guest)
        for index in range(3):
            body, screenshot = wait_page(guest, paths[-1], index)
            check_link_cue(screenshot, index < 2)
            screenshots.append(str(screenshot))
            link = re.search(r'<a href="([^"]+)">', body)
            if index < 2:
                if link is None or link[1] in paths:
                    raise ValueError(f"Fixture did not provide a distinct link in {body!r}")
                paths.append(link[1])
                guest.key_send("ret")
            elif link is not None:
                raise ValueError("The terminal page unexpectedly has a link")

        guest.key_send("ret")
        sleep(0.5)
        if len(read_requests(guest)) != 3:
            raise ValueError("Empty Enter made a request on the terminal page")

        paths.append("/index.html")
        guest.key_type(paths[-1])
        guest.key_send("ret")
        _, screenshot = wait_page(guest, paths[-1], 3)
        check_link_cue(screenshot, True)
        screenshots.append(str(screenshot))
    finally:
        guest.stop()

    requests = [data.split(b"\r\n", 1)[0] for src, _, _, dst, _, _, _, data
                in segments(guest.run / "network.pcap")
                if src == GUEST_IP and dst == HTTP_PORT and data.startswith(b"GET ")]
    if requests != [f"GET {path} HTTP/1.0".encode() for path in paths]:
        raise ValueError(f"Unexpected link navigation in PCAP: {requests!r}")
    print(json.dumps({"run": str(guest.run), "paths": paths, "screenshots": screenshots}))


if __name__ == "__main__":
    main()
