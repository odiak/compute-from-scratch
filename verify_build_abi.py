"""Exercise the compiler ABI with an observer-written guest assembly fixture."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt

COMPILER = (
    "ldrb w6,[x1];cmp w6,33;b.eq reject;lsl w6,w6,10;adr x5,template;ldr w5,[x5];orr w5,w5,w6;"
    "str w5,[x3];adr x5,tail;ldr w5,[x5];str w5,[x3,4];mov w0,8;ret;"
    "reject:;mov w0,0;ret;template:;.word 285212704;tail:;.word 3596551104"
).encode()


def main():
    root = Path(".local/build-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"save stub " + COMPILER[:64], b"saved\n")
        for offset in range(64, len(COMPILER), 64):
            command(guest, b"append stub " + COMPILER[offset:offset+64], b"saved\n")
        command(guest, b"as stub", b"assembled\n")
        command(guest, b"install", b"installed\n")
        value = secrets.randbelow(24) + 65
        command(guest, b"save src " + bytes([value]), b"saved\n")
        command(guest, b"build src", b"built\n")
        for argument in (secrets.randbelow(1000) + 1, secrets.randbelow(1000) + 1001):
            command(guest, f"run {argument}".encode(), f"exit {value + argument:08x}\n".encode())
        command(guest, b"save src Z", b"saved\n")
        command(guest, b"build src", b"built\n")
        command(guest, b"run 17", b"exit 0000006b\n")
        command(guest, b"save src !", b"saved\n")
        command(guest, b"build src", b"build error\n")
        command(guest, b"run 17", b"exit 0000006b\n")
    finally:
        guest.stop()
    print(f"Build ABI verified: {workspace}")


if __name__ == "__main__":
    main()
