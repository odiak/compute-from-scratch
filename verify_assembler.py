"""Verify guest-side assembly of runtime-supplied source."""
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_shell import command, read_prompt


def main():
    root = Path(".local/asm-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    qmp_dir = tempfile.TemporaryDirectory(dir="/tmp")
    socket = Path(qmp_dir.name) / "qmp.sock"
    try:
        guest.boot(disk=True, observer_socket=socket)
        read_prompt(guest)
        value = secrets.randbelow(900) + 100
        delta = secrets.randbelow(50) + 1
        mov = 0x52800000 | value << 5
        add = 0x11000000 | delta << 10
        sub = 0x51000000 | delta << 10
        ret = 0xd65f03c0
        for source, result, words in (
            (f"mov {value};b done;mov 0;done:;add {delta};ret", value + delta,
             [mov, 0x14000002, 0x52800000, add, ret]),
            (f"b start;mov 0;start:;mov {value};sub {delta};add 2;ret", value - delta + 2,
             [0x14000002, 0x52800000, mov, sub, 0x11000800, ret]),
            (f"mov {value};sub {delta};ret", value - delta, [mov, sub, ret]),
        ):
            command(guest, b"save test " + source.encode(), b"saved\n")
            command(guest, b"asm test", b"assembled\n")
            code = struct.pack("<" + "I" * len(words), *words)
            actual = read_memory(socket, 0x40106000, len(code), guest.run / "assembled.bin")
            if actual != code:
                raise ValueError(f"Unexpected AArch64 code: {actual.hex()} != {code.hex()}")
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
        qmp_dir.cleanup()
    print(f"Assembler verified: {workspace}")


if __name__ == "__main__":
    main()
