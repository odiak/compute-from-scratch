"""Verify that physical keyboard input drives HTTP navigation in one guest boot."""
import json
import re
import secrets
import sys
import tempfile
from pathlib import Path
from time import monotonic, sleep

from arp_link import GUEST_IP
from guest_tool import Guest
from tcp_peer import HTTP_PORT
from verify_browser import recognize
from verify_shell import read_prompt
from verify_tcp import segments


def read_requests(guest):
    log = guest.run / "http.jsonl"
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def check_screen(guest, expected):
    deadline = monotonic() + 6
    while monotonic() < deadline:
        screenshot = guest.display.capture(guest.run)
        actual = (recognize(screenshot, True), recognize(screenshot, False))
        if actual == expected:
            return screenshot
        sleep(0.1)
    raise ValueError(f"Rendered {actual}, expected {expected}")


def main():
    root = Path(".local/browser-path-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    guest = Guest(workspace)
    first = f"/a{secrets.token_hex(3)}7"
    second = f"/b{secrets.token_hex(8)}7-x.xy"
    screenshots = []
    bodies = []
    try:
        guest.boot(network=True, http=True, disk=True, display=True, browser=True, paths=True)
        read_prompt(guest)
        for path in (first, second, first):
            before = len(read_requests(guest))
            guest.key_type(path)
            guest.key_send("ret")
            request_line = f"GET {path} HTTP/1.0"
            deadline = monotonic() + 6
            while monotonic() < deadline:
                requests = read_requests(guest)[before:]
                matches = [row for row in requests if row["request"] == request_line]
                if matches:
                    break
                sleep(0.05)
            else:
                raise ValueError(f"Origin did not receive {request_line!r}. Observed {requests!r}")
            body = matches[-1]["body"]
            expected = re.search(r"<h1>([A-Z ]+)</h1><p>([A-Z ]+)</p>", body).groups()
            screenshots.append(str(check_screen(guest, expected)))
            bodies.append(body)
    finally:
        guest.stop()

    if bodies[0] == bodies[1] or bodies[0] != bodies[2]:
        raise ValueError("Origin did not serve distinct stable pages")
    requests = [data.split(b"\r\n", 1)[0] for src, _, _, dst, _, _, _, data
                in segments(guest.run / "network.pcap")
                if src == GUEST_IP and dst == HTTP_PORT and data.startswith(b"GET ")]
    expected = [f"GET {path} HTTP/1.0".encode() for path in (first, second, first)]
    if [request for request in requests if request in expected] != expected:
        raise ValueError(f"Unexpected keyboard navigation in PCAP: {requests!r}")
    print(json.dumps({"run": str(guest.run), "paths": [first, second, first],
                      "screenshots": screenshots, "pages": bodies}))


if __name__ == "__main__":
    main()
