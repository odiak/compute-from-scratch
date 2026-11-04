"""Verify guest HTML fetching and actual text on the framebuffer."""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from arp_link import GUEST_IP, PEER_IP
from guest_tool import Guest
from tcp_peer import HTTP_PORT, MASK
from verify_shell import command, read_prompt
from verify_tcp import segments


def recognize(screenshot, top):
    crop = "160x60+0+0" if top else "160x60+0+60"
    scaled = subprocess.check_output([
        "magick", str(screenshot), "-crop", crop, "+repage",
        "-colorspace", "gray", "-negate", "-filter", "Triangle", "-resize", "300%", "png:-",
    ])
    result = subprocess.run(
        ["tesseract", "stdin", "stdout", "--psm", "7", "-c",
         "tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ "],
        input=scaled, capture_output=True, check=True,
    )
    return " ".join(result.stdout.decode().upper().split())


def check_wire(run):
    request, = [json.loads(line) for line in (run / "http.jsonl").read_text().splitlines()]
    if request["request"] != "GET /index.html HTTP/1.0":
        raise ValueError("HTML request did not reach the host origin")
    body = request["body"].encode()
    packets = list(segments(run / "network.pcap"))
    if not any(src == GUEST_IP and dst == HTTP_PORT and data.startswith(b"GET /index.html HTTP/1.0\r\n")
               for src, _, _, dst, _, _, _, data in packets):
        raise ValueError("HTML request missing from PCAP")
    for index, (src, _, port, dst, seq, _, flags, data) in enumerate(packets):
        if src != PEER_IP or port != HTTP_PORT or not flags & 1:
            continue
        if not data.startswith(b"HTTP/1.0 200 ") or data.partition(b"\r\n\r\n")[2] != body:
            continue
        if any(src == GUEST_IP and port == dst and target == HTTP_PORT and flags & 16
               and ack == (seq + len(data) + 1) & MASK
               for src, _, port, target, _, ack, flags, _ in packets[index+1:]):
            return tuple(text.decode() for text in re.fullmatch(
                rb"<html><body><h1>([A-Z ]+)</h1><p>([A-Z ]+)</p></body></html>", body
            ).groups())
    raise ValueError("Actual HTML response or FIN acknowledgement missing from PCAP")


def main():
    root = Path(".local/browser-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    pages = set()
    for _ in range(8):
        guest.boot(network=True, http=True, disk=True, display=True, browser=True)
        try:
            read_prompt(guest)
            command(guest, b"echo browser", b"browser\n")
            screenshot = guest.display.capture(guest.run)
        finally:
            guest.stop()
        expected = check_wire(guest.run)
        actual = (recognize(screenshot, True), recognize(screenshot, False))
        print(json.dumps({"run": str(guest.run), "screenshot": str(screenshot),
                          "expected": expected, "ocr": actual}), flush=True)
        if actual != expected:
            raise ValueError("Screen text differs from host HTML")
        pages.add(expected)
        if len(pages) == 2:
            return
    raise ValueError("Did not observe two different pages")


if __name__ == "__main__":
    main()
