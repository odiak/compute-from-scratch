"""Verify migration from 16 occupied slots and the expanded source pipeline."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_process_io import application
from verify_shell import command, read_prompt
from verify_source_import import receive


def check_files(guest, files):
    for name, content in files.items():
        command(guest, b"cat " + name, content + b"\n")


def main():
    root = Path(".local/storage-growth-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    image = workspace / "guest.hex"
    image.write_bytes(Path(sys.argv[1]).read_bytes())
    guest = Guest(workspace)
    old = {
        f"old{i}".encode(): secrets.token_bytes(8192 if i in (0, 15) else i*11)
        for i in range(16)
    }
    bias = secrets.randbelow(40) + 2
    files = {
        b"n0": b"AZQ",
        b"wide": bytes(range(256)) + secrets.token_bytes(32768 - 256),
        b"asm": b" " * 9000 + f"mov w0,{bias};ret;".encode(),
        b"compiler": Path(sys.argv[3]).read_bytes().strip(),
        b"code": b" " * 16000 + f"int f(int x){{int total=x+{bias};return total;}}".encode(),
        b"read": application(b"n0"),
        b"spare1": b"",
        b"spare2": secrets.token_bytes(97),
    }
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        for name, content in old.items():
            receive(guest, name, content)
        guest.stop()

        image.write_bytes(Path(sys.argv[2]).read_bytes())
        guest.boot(disk=True)
        read_prompt(guest)
        check_files(guest, old)
        for name, content in files.items():
            receive(guest, name, content)
        command(guest, b"save overflow full", b"store full\n")
        command(guest, b"save spare2 changed", b"saved\n")
        command(guest, b"append spare2 tail", b"saved\n")
        files[b"spare2"] = b"changedtail"
        guest.serial_send(b"recv wide 32769\n".hex())
        rejected = read_prompt(guest)
        if b"ready\n" in rejected or rejected == b"shell> ":
            raise ValueError("Oversized import was not rejected")
        guest.stop()

        guest.boot(disk=True)
        read_prompt(guest)
        check_files(guest, old | files)
        command(guest, b"as asm", b"assembled\n")
        command(guest, b"run", f"exit {bias:08x}\n".encode())
        command(guest, b"as compiler", b"assembled\n")
        command(guest, b"install", b"installed\n")
        command(guest, b"build code", b"built\n")
        command(guest, b"run 93", f"exit {93+bias:08x}\n".encode())
        command(guest, b"as read", b"assembled\n")
        command(guest, b"spawn 37", b"pid 1\n")
        guest.serial_send(b"schedule\n".hex())
        if b"AZQ" not in read_prompt(guest):
            raise ValueError("Process did not read a file beyond the original 16 slots")
        command(guest, b"wait 1", b"exit 00000025\n")
    finally:
        guest.stop()
    print(f"Expanded storage verified: {workspace}")


if __name__ == "__main__":
    main()
