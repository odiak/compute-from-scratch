"""Verify filesystem migration, multi-sector persistence and larger guest programs."""
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt


def main():
    root = Path(".local/capacity-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    image = workspace / "guest.hex"
    legacy = Path(__file__).with_name("experiments") / "009-campaign.hex"
    image.write_text(legacy.read_text())
    guest = Guest(workspace)
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        legacy_text = b"legacy " + secrets.token_hex(8).encode()
        command(guest, b"save old " + legacy_text, b"saved\n")
        guest.stop()

        image.write_text(Path(sys.argv[1]).read_text())
        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"cat old", legacy_text + b"\n")
        chunks = [secrets.token_hex(32).encode() for _ in range(64)]
        command(guest, b"save large " + chunks[0], b"saved\n")
        for chunk in chunks[1:]:
            command(guest, b"append large " + chunk, b"saved\n")
        expected = b"".join(chunks)
        command(guest, b"cat large", expected + b"\n")
        guest.serial_send(b"append large x\n".hex())
        read_prompt(guest)
        command(guest, b"cat large", expected + b"\n")

        status = secrets.randbelow(65536)
        instructions = [0xd503201f] * 510 + [0x52800000 | status << 5, 0xd65f03c0]
        program = struct.pack("<" + "I" * len(instructions), *instructions).hex().encode()
        command(guest, b"save app " + program[:64], b"saved\n")
        for i in range(64, len(program), 64):
            command(guest, b"append app " + program[i:i+64], b"saved\n")
        guest.stop()

        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"cat old", legacy_text + b"\n")
        command(guest, b"cat large", expected + b"\n")
        command(guest, b"loadfile app", b"loaded\n")
        command(guest, b"run", f"exit {status:08x}\n".encode())
    finally:
        guest.stop()
    print(f"Capacity verified: {workspace}")


if __name__ == "__main__":
    main()
