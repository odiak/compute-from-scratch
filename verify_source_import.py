"""Verify raw source import, legacy disk migration and binary file persistence."""
import secrets
import sys
import tempfile
from pathlib import Path
from time import sleep

from guest_tool import Guest
from verify_shell import command, read_prompt


def receive(guest, name, data):
    line = b"recv " + name + f" {len(data)}\n".encode()
    if guest.serial_send(line.hex())["sent"] != len(line):
        raise ValueError("Could not send recv command")
    output = bytearray()
    while b"ready\n" not in output:
        part = bytes.fromhex(guest.serial_read(1000)["hex"])
        if not part or output.endswith(b"shell> "):
            raise ValueError(f"Guest refused to receive: {bytes(output)!r}")
        output.extend(part)
    _, _, remainder = bytes(output).partition(b"ready\n")
    for offset in range(0, len(data), 256):
        chunk = data[offset:offset+256]
        for _ in range(100):
            try:
                sent = guest.serial_send(chunk.hex())["sent"]
            except BlockingIOError:
                sleep(0.01)
                continue
            if sent != len(chunk):
                raise ValueError("Incomplete raw input write")
            break
        else:
            raise ValueError("Guest did not accept raw input")
    response = remainder if remainder.endswith(b"shell> ") else remainder + read_prompt(guest)
    if response != b"saved\nshell> ":
        raise ValueError("Guest did not save imported file")


def main():
    root = Path(".local/source-import-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    image = workspace / "guest.hex"
    image.write_text(Path("experiments/020-campaign.hex").read_text())
    guest = Guest(workspace)
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        legacy = b"legacy " + secrets.token_hex(8).encode()
        command(guest, b"save old " + legacy, b"saved\n")
        guest.stop()

        image.write_text(Path(sys.argv[1]).read_text())
        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"cat old", legacy + b"\n")
        source = b"int f(int x) {\n\treturn x + 1;\n}\n"
        data = bytes(range(256)) + secrets.token_bytes(8192 - 256)
        receive(guest, b"src", source)
        receive(guest, b"raw", data)
        receive(guest, b"zero", b"")
        guest.serial_send(b"recv raw 8193\n".hex())
        rejected = read_prompt(guest)
        if b"ready\n" in rejected or rejected == b"shell> ":
            raise ValueError("Oversized import was not rejected")
        guest.stop()

        guest.boot(disk=True)
        read_prompt(guest)
        for name, content in ((b"old", legacy), (b"src", source), (b"raw", data), (b"zero", b"")):
            command(guest, b"cat " + name, content + b"\n")
    finally:
        guest.stop()
    print(f"Source import verified: {workspace}")


if __name__ == "__main__":
    main()
