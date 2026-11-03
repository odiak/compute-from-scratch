"""Check named-file persistence across boots of an experiment image."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt


def boot(guest, disk):
    guest.boot(disk=disk)
    if not read_prompt(guest).startswith(b"BOOT\n"):
        raise ValueError("Missing boot banner")


def main():
    root = Path(".local/disk-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    name_a = b"a" + secrets.token_hex(5).encode()
    name_b = b"b" + secrets.token_hex(5).encode()
    value_a = b"first " + secrets.token_hex(8).encode()
    value_b = b"second " + secrets.token_hex(8).encode()
    updated = b"replacement " + secrets.token_hex(8).encode()
    try:
        boot(guest, False)
        for line in (b"ls", b"cat " + name_a, b"save " + name_a + b" x"):
            command(guest, line, b"no disk\n")
        guest.stop()

        boot(guest, True)
        command(guest, b"ls", b"")
        command(guest, b"cat " + name_a, b"not found\n")
        command(guest, b"save " + name_a + b" " + value_a, b"saved\n")
        command(guest, b"save " + name_b + b" " + value_b, b"saved\n")
        guest.stop()

        boot(guest, True)
        command(guest, b"cat " + name_a, value_a + b"\n")
        command(guest, b"cat " + name_b, value_b + b"\n")
        guest.serial_send(b"ls\n".hex())
        listed = read_prompt(guest).removesuffix(b"shell> ").splitlines()
        if sorted(listed) != sorted([name_a, name_b]):
            raise ValueError(f"Unexpected file listing: {listed!r}")
        command(guest, b"save " + name_a + b" " + updated, b"saved\n")
        guest.stop()

        boot(guest, True)
        command(guest, b"cat " + name_a, updated + b"\n")
        command(guest, b"cat " + name_b, value_b + b"\n")
        command(guest, b"echo still alive", b"still alive\n")
    finally:
        guest.stop()
    print(f"Disk verified: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
