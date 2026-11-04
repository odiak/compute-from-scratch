"""Reproduce and compare three generations of a guest assembler."""
import hashlib
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_subset import put_file
from verify_shell import command, read_prompt


def snapshot(guest, socket, generation):
    size = int.from_bytes(read_memory(socket, 0x40142004, 4, guest.run / "size.bin"), "little")
    if not 4 <= size <= 2048 or size % 4:
        raise ValueError(f"Unexpected assembled length: {size}")
    return read_memory(socket, 0x40140000, size, guest.run / f"generation-{generation}.bin")


def main():
    root = Path(".local/self-host-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    source = Path(sys.argv[2]).read_bytes().strip()
    guest = Guest(workspace)
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            put_file(guest, b"asrc", source)
            command(guest, b"as asrc", b"assembled\n")
            seed = snapshot(guest, socket, 0)
            command(guest, b"install", b"installed\n")
            command(guest, b"build asrc", b"built\n")
            first = snapshot(guest, socket, 1)
            command(guest, b"install", b"installed\n")
            command(guest, b"build asrc", b"built\n")
            second = snapshot(guest, socket, 2)
            if seed != first or first != second:
                raise ValueError("Assembler generations differ")
            value = secrets.randbelow(1024) + 1
            delta = secrets.randbelow(127) + 1
            sample = f"mov w0,{value};b end;mov w0,0;end:;add w0,w0,{delta};ret;"
            put_file(guest, b"sample", sample.encode())
            command(guest, b"build sample", b"built\n")
            expected = struct.pack("<5I", 0x52800000 | value << 5, 0x14000002,
                                   0x52800000, 0x11000000 | delta << 10, 0xd65f03c0)
            if snapshot(guest, socket, "sample") != expected:
                raise ValueError("Independent sample machine code differs")
            command(guest, b"run", f"exit {value + delta:08x}\n".encode())
        finally:
            guest.stop()
    print(f"Self-host verified: {len(seed)} bytes, sha256={hashlib.sha256(seed).hexdigest()}, {workspace}")


if __name__ == "__main__":
    main()
