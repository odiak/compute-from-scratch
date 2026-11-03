"""Build C-subset functions with the supplied guest-assembly compiler."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_shell import command, read_prompt


def put_file(guest, name, source):
    command(guest, b"save " + name + b" " + source[:64], b"saved\n")
    for offset in range(64, len(source), 64):
        command(guest, b"append " + name + b" " + source[offset:offset+64], b"saved\n")


def main():
    root = Path(".local/c-subset-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    compiler = Path(sys.argv[2]).read_bytes().strip()
    guest = Guest(workspace)
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            put_file(guest, b"compiler", compiler)
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            a, b = [secrets.randbelow(60) + 3 for _ in range(2)]
            for expression, calculate in (
                (f"x+{a}*{b}", lambda x: x + a * b),
                (f"(x+{a})*{b}", lambda x: (x + a) * b),
                (f"{a}-x-{b}", lambda x: a - x - b),
            ):
                source = f"int f(int x){{return {expression};}}".encode()
                put_file(guest, b"expr", source)
                command(guest, b"build expr", b"built\n")
                dump = guest.run / "compiled.bin"
                before = read_memory(socket, 0x40140000, 2048, dump)
                for argument in (secrets.randbelow(80) + 1, secrets.randbelow(100) + 100):
                    result = calculate(argument) & 0xffffffff
                    command(guest, f"run {argument}".encode(), f"exit {result:08x}\n".encode())
                if read_memory(socket, 0x40140000, 2048, dump) != before:
                    raise ValueError("Generated machine code changed between runtime inputs")
            put_file(guest, b"expr", b"int f(int x){return (x+);}")
            command(guest, b"build expr", b"build error\n")
            command(guest, b"run 19", f"exit {(a - 19 - b) & 0xffffffff:08x}\n".encode())
        finally:
            guest.stop()
    print(f"C-subset compiler verified: {workspace}")


if __name__ == "__main__":
    main()
