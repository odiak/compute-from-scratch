"""Verify that the guest compiler emits runtime branches and loops."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_subset import put_file
from verify_shell import command, read_prompt


def main():
    root = Path(".local/c-control-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    compiler = Path(sys.argv[2]).read_bytes().strip()
    guest = Guest(workspace)
    start = secrets.randbelow(40) + 5
    delta = secrets.randbelow(12) + 2
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            put_file(guest, b"compiler", compiler)
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            programs = [
                (f"int f(int x){{int y={start};while(x){{y=y+{delta};x=x-1;}}return y;}}",
                 lambda x: start + delta * x),
                (f"int f(int x){{int y={start};if(x){{y=y+{delta};}}return y;}}",
                 lambda x: start + (delta if x else 0)),
                (f"int f(int x){{int y={start};if(x){{y=y+1;}}while(x){{y=y+x;x=x-1;}}return y;}}",
                 lambda x: start + bool(x) + x * (x + 1) // 2),
            ]
            for source, calculate in programs:
                put_file(guest, b"test", source.encode())
                command(guest, b"build test", b"built\n")
                dump = guest.run / "compiled.bin"
                code = read_memory(socket, 0x40140000, 2048, dump)
                for argument in (0, secrets.randbelow(8) + 1, secrets.randbelow(8) + 9):
                    command(guest, f"run {argument}".encode(), f"exit {calculate(argument):08x}\n".encode())
                if read_memory(socket, 0x40140000, 2048, dump) != code:
                    raise ValueError("Generated code changed between runtime inputs")
            put_file(guest, b"test", b"int f(int x){int y=0;while(x){y=;}return y;}")
            command(guest, b"build test", b"build error\n")
            command(guest, b"run 3", f"exit {start + 7:08x}\n".encode())
        finally:
            guest.stop()
    print(f"C control flow verified: {workspace}")


if __name__ == "__main__":
    main()
