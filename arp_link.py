"""Private Ethernet peer for the ARP experiment."""
from contextlib import suppress
import secrets
import socket
from threading import Thread

PEER_IP = bytes([10, 0, 2, 2])
GUEST_IP = bytes([10, 0, 2, 15])
ARP_REQUEST = bytes.fromhex("0001080006040001")
ARP_REPLY = bytes.fromhex("0001080006040002")


class ArpLink:
    def __init__(self):
        self.mac = b"\x02" + secrets.token_bytes(5)
        self.host, self.guest = socket.socketpair()
        self.thread = Thread(target=self.serve, daemon=True)

    def serve(self):
        with self.host.makefile("rb") as stream:
            try:
                while header := stream.read(4):
                    frame = stream.read(int.from_bytes(header, "big"))
                    if (len(frame) >= 42 and frame[12:22] == b"\x08\x06" + ARP_REQUEST
                            and frame[28:32] == GUEST_IP and frame[38:42] == PEER_IP):
                        sender = frame[22:28]
                        reply = (sender + self.mac + b"\x08\x06" + ARP_REPLY
                                 + self.mac + PEER_IP + sender + GUEST_IP)
                        reply = reply.ljust(60, b"\0")
                        self.host.sendall(len(reply).to_bytes(4, "big") + reply)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def close(self):
        self.guest.close()
        with suppress(OSError):
            self.host.shutdown(socket.SHUT_RDWR)
        if self.thread.ident is not None:
            self.thread.join()
        self.host.close()
