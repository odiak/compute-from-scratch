"""Exercise the larger assembler with a loop, multiple registers and a call."""
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_shell import command, read_prompt


def main():
    root = Path(".local/as-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    count = secrets.randbelow(15) + 3
    delta = secrets.randbelow(50) + 2
    source = (
        f"mov w0,0;mov w3,{count};loop:;add w0,w0,{delta};"
        "sub w3,w3,1;cmp w3,0;b.ne loop;"
        "mov x9,x30;bl fn;mov x30,x9;b end;"
        f"fn:;add w0,w0,{delta};ret;end:;"
        + "add w0,w0,1;" * 20 + "ret"
    ).encode()
    qmp_dir = tempfile.TemporaryDirectory(dir="/tmp")
    socket = Path(qmp_dir.name) / "qmp.sock"
    try:
        guest.boot(disk=True, observer_socket=socket)
        read_prompt(guest)
        command(guest, b"save test " + source[:64], b"saved\n")
        for offset in range(64, len(source), 64):
            command(guest, b"append test " + source[offset:offset+64], b"saved\n")
        command(guest, b"as test", b"assembled\n")
        add = 0x11000000 | delta << 10
        words = [
            0x52800000, 0x52800003 | count << 5, add, 0x51000463,
            0x7100007f, 0x54ffffa1, 0xaa1e03e9, 0x94000003,
            0xaa0903fe, 0x14000003, add, 0xd65f03c0,
            *([0x11000400] * 20), 0xd65f03c0,
        ]
        code = struct.pack("<" + "I" * len(words), *words)
        actual = read_memory(socket, 0x40140000, len(code), guest.run / "assembled.bin")
        if actual != code:
            raise ValueError(f"Unexpected AArch64 code: {actual.hex()} != {code.hex()}")
        command(guest, b"run", f"exit {(count + 1) * delta + 20:08x}\n".encode())
    finally:
        guest.stop()
        qmp_dir.cleanup()
    print(f"General assembler verified: {workspace}")


if __name__ == "__main__":
    main()
