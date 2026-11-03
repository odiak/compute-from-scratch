"""Verify guest-side assembly of runtime-supplied source."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt


def main():
    root = Path(".local/asm-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        value = secrets.randbelow(900) + 100
        delta = secrets.randbelow(50) + 1
        for source, result in (
            (f"mov {value};b done;mov 0;done:;add {delta};ret", value + delta),
            (f"b start;mov 0;start:;mov {value};sub {delta};add 2;ret", value - delta + 2),
            (f"mov {value};sub {delta};ret", value - delta),
        ):
            command(guest, b"save test " + source.encode(), b"saved\n")
            command(guest, b"asm test", b"assembled\n")
            expected = f"exit {result:08x}\n".encode()
            command(guest, b"run", expected)
        command(guest, b"save bad b absent;ret", b"saved\n")
        command(guest, b"asm bad", b"assembly error\n")
        command(guest, b"run", expected)
        guest.stop()
        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"asm test", b"assembled\n")
        command(guest, b"run", expected)
    finally:
        guest.stop()
    print(f"Assembler verified: {workspace}")


if __name__ == "__main__":
    main()
