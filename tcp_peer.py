"""Single-connection TCP challenge service for the private experiment link."""
import secrets
import struct

from arp_link import GUEST_IP, PEER_IP

PORT = 2323
HTTP_PORT = 8080
MASK = 0xffffffff


def checksum(data):
    if len(data) % 2:
        data += b"\0"
    total = sum(word for word, in struct.iter_unpack("!H", data))
    while total >> 16:
        total = (total & 0xffff) + (total >> 16)
    return total ^ 0xffff


def pseudo(src, dst, length):
    return struct.pack("!4s4sBBH", src, dst, 0, 6, length)


class TcpPeer:
    def __init__(self, mac, http=None):
        self.mac = mac
        self.http = http
        self.service_port = HTTP_PORT if http else PORT
        self.isn = secrets.randbits(32)
        self.challenge = b"ECHO ping " + secrets.token_hex(6).encode() + b"\n"
        self.port = None
        self.guest_next = None
        self.responded = False

    def packet(self, mac, seq, ack, flags, data=b""):
        tcp = struct.pack("!HHIIBBHHH", self.service_port, self.port, seq, ack, 0x50, flags, 4096, 0, 0) + data
        crc = checksum(pseudo(PEER_IP, GUEST_IP, len(tcp)) + tcp)
        tcp = tcp[:16] + struct.pack("!H", crc) + tcp[18:]
        ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(tcp), 0, 0, 64, 6, 0,
                         PEER_IP, GUEST_IP)
        ip = ip[:10] + struct.pack("!H", checksum(ip)) + ip[12:]
        return (mac + self.mac + b"\x08\x00" + ip + tcp).ljust(60, b"\0")

    def receive(self, frame):
        ip = frame[14:]
        if (len(ip) < 40 or frame[:6] != self.mac or frame[12:14] != b"\x08\x00"
                or ip[0] != 0x45 or ip[9] != 6 or ip[12:20] != GUEST_IP + PEER_IP
                or checksum(ip[:20])):
            return None
        total = int.from_bytes(ip[2:4], "big")
        if not 40 <= total <= len(ip) or int.from_bytes(ip[6:8], "big") & 0x3fff:
            return None
        tcp = ip[20:total]
        if checksum(pseudo(GUEST_IP, PEER_IP, len(tcp)) + tcp):
            return None
        src, dst, seq, ack, offset, flags = struct.unpack_from("!HHIIBB", tcp)
        header = (offset >> 4) * 4
        if dst != self.service_port or not 20 <= header <= len(tcp):
            return None
        if flags == 2 and self.port is None:
            self.port = src
            self.guest_next = (seq + 1) & MASK
        if flags == 2 and self.port == src and self.guest_next == (seq + 1) & MASK:
            return self.packet(frame[6:12], self.isn, self.guest_next, 0x12)
        server_next = (self.isn + 1) & MASK
        if src != self.port or not flags & 0x10 or ack != server_next:
            return None
        if self.responded or seq != self.guest_next:
            return None
        data = tcp[header:]
        if self.http:
            request_line = f"GET {self.http.path} HTTP/1.0\r\n".encode()
            if not (data.startswith(request_line)
                    and data.endswith(b"\r\n\r\n") and len(data) <= 1024):
                return None
            payload, response_flags = self.http.request(data), 0x19
        else:
            if data != b"ping\n":
                return None
            payload, response_flags = self.challenge, 0x18
        self.guest_next = (seq + len(data)) & MASK
        self.responded = True
        return self.packet(frame[6:12], server_next, self.guest_next, response_flags, payload)
