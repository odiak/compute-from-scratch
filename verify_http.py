"""Check that the guest fetched and displayed the host origin's actual response."""
import json
import sys
from pathlib import Path

from arp_link import GUEST_IP, PEER_IP
from tcp_peer import HTTP_PORT, MASK
from verify_tcp import segments


def verify(run):
    access_log = run / "http.jsonl"
    requests = [json.loads(line) for line in access_log.read_text().splitlines()] if access_log.exists() else []
    expected = requests[0]["body"].encode() if len(requests) == 1 else b""
    output = (run / "serial.log").read_bytes()
    packets = list(segments(run / "network.pcap"))
    get = any(src == GUEST_IP and dst_port == HTTP_PORT
              and data.startswith(b"GET /hello HTTP/1.0\r\n") and data.endswith(b"\r\n\r\n")
              for src, _, _, dst_port, _, _, _, data in packets)
    response = any(
        expected and src == PEER_IP and port == HTTP_PORT and flags & 1
        and data.startswith(b"HTTP/1.0 200 ") and data.partition(b"\r\n\r\n")[2] == expected
        and any(
            ack_src == GUEST_IP and ack_port == dst_port and ack_dst == HTTP_PORT
            and ack_flags & 16 and ack == (seq + len(data) + 1) & MASK
            for ack_src, _, ack_port, ack_dst, _, ack, ack_flags, _ in packets[i+1:]
        )
        for i, (src, _, port, dst_port, seq, _, flags, data) in enumerate(packets)
    )
    origin = len(requests) == 1 and requests[0]["request"] == "GET /hello HTTP/1.0"
    record = json.loads((run / "run.json").read_text())
    mac = record["peer_mac"].encode() + b"\n"
    serial = bool(expected and output.startswith(b"BOOT\n" + mac) and expected in output.splitlines(keepends=True))
    print(json.dumps({"get": get, "origin": origin, "response_and_fin_ack": response,
                      "serial": serial, "serial_hex": output.hex()}))
    return all((get, origin, response, serial))


if __name__ == "__main__":
    raise SystemExit(0 if verify(Path(sys.argv[1])) else 1)
