"""Verify guest-assembled address, stack, memory and data operations."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt


def main():
    root = Path(".local/as-memory-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    value = secrets.randbelow(0xffffffff)
    factor = secrets.randbelow(15) + 2
    source = (
        "sub sp,sp,16;adr x3,data;ldr w4,[x3];str w4,[sp,4];"
        "ldrb w0,[sp,5];mov w1," + str(factor) + ";mul w0,w0,w1;"
        "add sp,sp,16;ret;data:;.word " + str(value)
    ).encode()
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"save test " + source[:64], b"saved\n")
        for offset in range(64, len(source), 64):
            command(guest, b"append test " + source[offset:offset+64], b"saved\n")
        command(guest, b"as test", b"assembled\n")
        command(guest, b"run", f"exit {((value >> 8) & 255) * factor:08x}\n".encode())
    finally:
        guest.stop()
    print(f"Memory operations verified: {workspace}")


if __name__ == "__main__":
    main()
