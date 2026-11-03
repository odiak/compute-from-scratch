"""Verify a TCP challenge, its acknowledgement, and serial output from a run."""
import json
import struct
import sys
from pathlib import Path

from arp_link import GUEST_IP, PEER_IP
from tcp_peer import MASK, PORT, checksum, pseudo
from verify_arp import frames


def segments(path):
    for frame in frames(path):
        ip = frame[14:]
        if frame[12:14] != b"\x08\x00" or len(ip) < 40 or ip[0] != 0x45 or ip[9] != 6:
            continue
        if checksum(ip[:20]):
            continue
        source, target = ip[12:16], ip[16:20]
        tcp = ip[20:int.from_bytes(ip[2:4], "big")]
        if len(tcp) < 20 or checksum(pseudo(source, target, len(tcp)) + tcp):
            continue
        src_port, dst_port, seq, ack, offset, flags = struct.unpack_from("!HHIIBB", tcp)
        yield source, target, src_port, dst_port, seq, ack, flags, tcp[(offset >> 4) * 4:]


def verify(run):
    record = json.loads((run / "run.json").read_text())
    expected = record["tcp_challenge"].encode()
    output = (run / "serial.log").read_bytes()
    packets = list(segments(run / "network.pcap"))
    sent = any(source == GUEST_IP and dst == PORT and data == b"ping\n"
               for source, _, _, dst, _, _, _, data in packets)
    acked = any(
        source == PEER_IP and src == PORT and data == expected and any(
            reply_source == GUEST_IP and reply_src == dst and reply_dst == PORT
            and flags & 0x10 and ack == (seq + len(data)) & MASK
            for reply_source, _, reply_src, reply_dst, _, ack, flags, _ in packets[i+1:]
        )
        for i, (source, _, src, dst, seq, _, _, data) in enumerate(packets)
    )
    handshake = any(
        source == GUEST_IP and dst == PORT and flags == 2 and any(
            reply_source == PEER_IP and reply_src == PORT and reply_dst == src
            and reply_flags == 0x12 and ack == (seq + 1) & MASK
            for reply_source, _, reply_src, reply_dst, _, ack, reply_flags, _ in packets[i+1:]
        )
        for i, (source, _, src, dst, seq, _, flags, _) in enumerate(packets)
    )
    serial = output.startswith(b"BOOT\n") and expected in output.splitlines(keepends=True)
    mac = record["peer_mac"].encode() + b"\n" in output.lower().splitlines(keepends=True)
    print(json.dumps({"handshake": handshake, "ping": sent, "ack": acked,
                      "serial": serial, "arp_mac": mac, "serial_hex": output.hex()}))
    return all((handshake, sent, acked, serial, mac))


if __name__ == "__main__":
    raise SystemExit(0 if verify(Path(sys.argv[1])) else 1)
