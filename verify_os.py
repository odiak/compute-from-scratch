"""Verify that the guest shell loads and executes programs supplied over serial."""
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_http import verify as verify_http
from verify_shell import command, read_prompt


def program(status, emit):
    instructions = [0x52800000 | status << 5, 0xd65f03c0]
    if emit:
        instructions = [
            0xa9bf7bfd,  # stp x29, x30, [sp, #-16]!
            0xaa0003e9,  # mov x9, x0
            0x52800420,  # mov w0, #'!'
            0xd63f0120,  # blr x9
            instructions[0],
            0xa8c17bfd,  # ldp x29, x30, [sp], #16
            instructions[1],
        ]
    return b"load " + struct.pack("<" + "I" * len(instructions), *instructions).hex().encode()


def main():
    root = Path(".local/os-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    for network in (False, True):
        guest.boot(network=network, http=network)
        try:
            read_prompt(guest)
            command(guest, b"help", b"help echo load run\n")
            command(guest, b"run", b"no program\n")
            code = secrets.randbelow(65536)
            command(guest, program(code, False), b"loaded\n")
            command(guest, b"run", f"exit {code:08x}\n".encode())
            command(guest, b"load 0000000g", b"invalid program\n")
            command(guest, b"run", f"exit {code:08x}\n".encode())
            code ^= 0xffff
            command(guest, program(code, True), b"loaded\n")
            command(guest, b"run", f"!exit {code:08x}\n".encode())
            command(guest, b"echo alive", b"alive\n")
        finally:
            guest.stop()
        if network and not verify_http(guest.run):
            return 1
        print(f"OS loader verified: {guest.run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
