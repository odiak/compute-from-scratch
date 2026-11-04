"""Verify live retrieval, exact persistence, and offline compilation of upstream C."""
import hashlib
import json
import secrets
import sys
import tempfile
from pathlib import Path

from arp_link import GUEST_IP, PEER_IP
from guest_tool import Guest
from release_origin import ARCHIVE_SHA256, ARCHIVE_URL, SOURCE_PATH, SOURCE_SHA256
from tcp_peer import HTTP_PORT, MASK
from verify_sbase_echo import build_upstream, check_echo
from verify_shell import command, read_prompt
from verify_source_import import receive
from verify_tcp import segments


def fetch(guest, path, name):
    line = b"fetch " + path.encode() + b" " + name + b"\n"
    if guest.serial_send(line.hex())["sent"] != len(line):
        raise ValueError("Could not send fetch command")
    return read_prompt(guest, timeout=20)


def check_wire(run, upstream, denied=False):
    rows = [json.loads(line) for line in (run / "release.jsonl").read_text().splitlines()]
    external = [row for row in rows if "upstream" in row]
    request = f"GET {SOURCE_PATH} HTTP/1.0"
    if external != [{
        "request": request, "upstream": ARCHIVE_URL, "archive_sha256": ARCHIVE_SHA256,
        "source_sha256": SOURCE_SHA256, "status": 200, "bytes": len(upstream),
    }]:
        raise ValueError(f"Unexpected release-origin log: {rows!r}")
    if denied and not any(row["request"] == "GET /denied HTTP/1.0" and row["status"] == 404
                          for row in rows):
        raise ValueError("Non-allowlisted path did not receive a local 404")
    packets = list(segments(run / "network.pcap"))
    if not any(src == GUEST_IP and dst == HTTP_PORT and data.startswith(request.encode() + b"\r\n")
               for src, _, _, dst, _, _, _, data in packets):
        raise ValueError("Guest GET did not appear on the private wire")
    for index, (src, _, port, dst, seq, _, flags, data) in enumerate(packets):
        headers, _, body = data.partition(b"\r\n\r\n")
        if src != PEER_IP or port != HTTP_PORT or not flags & 1:
            continue
        if not headers.startswith(b"HTTP/1.0 200 ") or body != upstream:
            continue
        if any(src == GUEST_IP and port == dst and target == HTTP_PORT and flags & 16
               and ack == (seq + len(data) + 1) & MASK
               for src, _, port, target, _, ack, flags, _ in packets[index+1:]):
            return
    raise ValueError("Exact source body and FIN acknowledgement missing from the private wire")


def check_full_disk(image, upstream):
    root = image.parent / "full"
    root.mkdir()
    (root / "guest.hex").write_bytes(image.read_bytes())
    guest = Guest(root)
    try:
        guest.boot(network=True, http=True, disk=True, release=True)
        read_prompt(guest)
        command(guest, b"save marker original", b"saved\n")
        for index in range(1, 24):
            command(guest, f"save hold{index} keep{index}".encode(), b"saved\n")
        fetch(guest, SOURCE_PATH, b"marker")
        command(guest, b"cat marker", upstream + b"\n")
        for index in range(1, 24):
            command(guest, f"cat hold{index}".encode(), f"keep{index}\n".encode())
        run = guest.run
    finally:
        guest.stop()
    check_wire(run, upstream)


def main():
    root = Path(".local/external-source-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    seed, base, cli, adapter, upstream = (Path(name).read_bytes() for name in sys.argv[2:7])
    reference = Path(sys.argv[7]).resolve()
    if hashlib.sha256(upstream).hexdigest() != SOURCE_SHA256:
        raise ValueError("Expected source is not the pinned upstream member")
    guest = Guest(workspace)
    name = b"src" + secrets.token_hex(3).encode()
    try:
        guest.boot(network=True, http=True, disk=True, release=True)
        read_prompt(guest)
        command(guest, b"cat " + name, b"not found\n")
        fetch(guest, SOURCE_PATH, name)
        command(guest, b"cat " + name, upstream + b"\n")
        fetch(guest, "/denied", name)
        command(guest, b"cat " + name, upstream + b"\n")
        network_run = guest.run
        guest.stop()

        check_wire(network_run, upstream, denied=True)

        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"cat " + name, upstream + b"\n")
        for file, source in ((b"seed", seed.strip()), (b"base", base), (b"cli", cli), (b"adapter", adapter)):
            receive(guest, file, source)
        build_upstream(guest, name)
        check_echo(guest, reference)
    finally:
        guest.stop()
    check_full_disk(workspace / "guest.hex", upstream)
    print(f"External release fetch and guest build verified: {workspace}")
    print(f"Network evidence: {network_run}")


if __name__ == "__main__":
    main()
