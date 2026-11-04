"""Exercise a large installed guest tool and an 8 KiB executable."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt
from verify_source_import import receive


def compiler_source(bias):
    # The entry branch skips 520 instruction words before the compiler body.
    # Its output enters through a branch to the final two instructions.
    add = 0x11000020 | bias << 10
    return (
        "b start;" + "ret;" * 520 +
        "start:;ldrb w0,[x1];cmp w0,33;b.eq oversized;"
        "mov w5,8192;cmp w4,w5;b.lt small;"
        "adr x6,code;ldr w0,[x6];str w0,[x3];"
        "mov w7,4;mov w8,8184;add x9,x3,4;"
        "fill:;str w0,[x9];add x9,x9,4;add w7,w7,4;cmp w7,w8;b.lt fill;"
        "ldr w0,[x6,4];str w0,[x3,8184];"
        "ldr w0,[x6,8];str w0,[x3,8188];mov w0,8192;ret;"
        "oversized:;mov w0,0;str w0,[x3];add w0,w4,4;ret;"
        f"small:;mov w0,0;ret;code:;.word {0x140007fe};.word {add};.word {0xd65f03c0};"
    ).encode()


def main():
    root = Path(".local/toolchain-capacity-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    guest = Guest(workspace)
    bias = secrets.randbelow(90) + 10
    for boot in range(2):
        try:
            guest.boot(disk=True)
            read_prompt(guest)
            if boot == 0:
                receive(guest, b"boundary", b"ret;" * 2048)
                receive(guest, b"compiler", compiler_source(bias))
                receive(guest, b"valid", b"+")
                receive(guest, b"invalid", b"!")
            command(guest, b"as boundary", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build valid", b"built\n")
            for argument in (0, secrets.randbelow(900) + 100):
                command(guest, f"run {argument}".encode(), f"exit {argument + bias:08x}\n".encode())
            command(guest, b"build invalid", b"build error\n")
            command(guest, b"run 29", f"exit {29 + bias:08x}\n".encode())
        finally:
            guest.stop()
    print(f"Toolchain capacity verified: {workspace}")


if __name__ == "__main__":
    main()
