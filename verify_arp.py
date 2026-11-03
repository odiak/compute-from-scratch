"""Replay a guest twice and verify ARP reception against private link captures."""
import argparse
import json
import re
import struct
import tempfile
from pathlib import Path
from time import monotonic

from arp_link import ARP_REPLY, ARP_REQUEST, GUEST_IP, PEER_IP
from guest_tool import Guest

GUEST_MAC = bytes.fromhex("525400123456")
MAC_LINE = re.compile(rb"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\n")


def frames(path):
    with path.open("rb") as pcap:
        magic = pcap.read(24)[:4]
        endian = {b"\xd4\xc3\xb2\xa1": "<", b"\xa1\xb2\xc3\xd4": ">"}[magic]
        while header := pcap.read(16):
            _, _, length, _ = struct.unpack(endian + "IIII", header)
            yield pcap.read(length)


def verify(guest, reference):
    guest.boot(network=True)
    output = b""
    deadline = monotonic() + 5
    try:
        while monotonic() < deadline and not MAC_LINE.search(output):
            output += bytes.fromhex(guest.serial_read(250)["hex"])
        if not reference and MAC_LINE.search(output):
            guest.serial_send("41")
            output += bytes.fromhex(guest.serial_read(1000)["hex"])
    finally:
        guest.stop()

    run = guest.run
    mac = json.loads((run / "run.json").read_text())["peer_mac"]
    wire_mac = bytes.fromhex(mac.replace(":", ""))
    request = (b"\xff" * 6 + GUEST_MAC + b"\x08\x06" + ARP_REQUEST
               + GUEST_MAC + GUEST_IP + b"\0" * 6 + PEER_IP)
    reply = (GUEST_MAC + wire_mac + b"\x08\x06" + ARP_REPLY
             + wire_mac + PEER_IP + GUEST_MAC + GUEST_IP)
    packets = list(frames(run / "network.pcap"))
    sent = any(packet.startswith(request) for packet in packets)
    received = any(packet.startswith(reply) for packet in packets)
    serial_matches = mac.encode() + b"\n" in output.lower().splitlines(keepends=True)
    passed = sent and received and serial_matches
    if not reference:
        passed = passed and output.startswith(b"BOOT\n") and output.endswith(b"\nA")
    print(json.dumps({"run": str(run), "request": sent, "reply": received,
                      "peer_mac": mac, "serial_hex": output.hex(), "passed": passed}), flush=True)
    return mac, passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--reference", action="store_true", help="skip boot and echo regression checks")
    args = parser.parse_args()
    root = Path(".local/arp-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(args.image.read_text())
    guest = Guest(workspace)
    results = [verify(guest, args.reference) for _ in range(2)]
    return 0 if all(passed for _, passed in results) and results[0][0] != results[1][0] else 1


if __name__ == "__main__":
    raise SystemExit(main())
