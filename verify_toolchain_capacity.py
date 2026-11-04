"""Exercise a large installed guest tool and a large generated executable."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt
from verify_source_import import receive


def compiler_source(bias, capacity):
    # Skip enough words to put the compiler body past the previous limit.
    # The generated program branches to its final two instructions.
    add = 0x11000020 | bias << 10
    branch = 0x14000000 | (capacity // 4 - 2)
    padding = capacity // 16 + 8
    return (
        "b start;" + "ret;" * padding +
        "start:;ldrb w0,[x1];cmp w0,33;b.eq oversized;"
        f"mov w5,{capacity};cmp w4,w5;b.lt small;"
        "adr x6,code;ldr w0,[x6];str w0,[x3];"
        f"mov w7,4;mov w8,{capacity-8};add x9,x3,4;"
        "fill:;str w0,[x9];add x9,x9,4;add w7,w7,4;cmp w7,w8;b.lt fill;"
        "ldr w0,[x6,4];str w0,[x9];"
        f"ldr w0,[x6,8];str w0,[x9,4];mov w0,{capacity};ret;"
        "oversized:;mov w0,0;str w0,[x3];add w0,w4,4;ret;"
        f"small:;mov w0,0;ret;code:;.word {branch};.word {add};.word {0xd65f03c0};"
    ).encode()


def main():
    root = Path(".local/toolchain-capacity-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    guest = Guest(workspace)
    bias = secrets.randbelow(90) + 10
    capacity = int(sys.argv[2]) if len(sys.argv) > 2 else 8192
    for boot in range(2):
        try:
            guest.boot(disk=True)
            read_prompt(guest)
            if boot == 0:
                receive(guest, b"boundary", b"ret;" * (capacity // 4))
                receive(guest, b"compiler", compiler_source(bias, capacity))
                receive(guest, b"valid", b"+")
                receive(guest, b"invalid", b"!")
            command(guest, b"as boundary", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build valid", b"built\n")
            for argument in (0, secrets.randbelow(900) + 100):
                command(guest, f"run {argument}".encode(), f"exit {argument + bias:08x}\n".encode())
            if capacity > 8192:
                command(guest, b"spawn 0", b"error\n")
            command(guest, b"build invalid", b"build error\n")
            command(guest, b"as invalid", b"assembly error\n")
            command(guest, b"run 29", f"exit {29 + bias:08x}\n".encode())
        finally:
            guest.stop()
    print(f"Toolchain capacity verified: {workspace}")


if __name__ == "__main__":
    main()
