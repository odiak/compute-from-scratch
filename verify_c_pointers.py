"""Verify a local int pointer and its alias through the guest compiler."""
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_c_functions import calls, generated_code
from verify_shell import command, read_prompt
from verify_source_import import receive


def has_stack_pointer_access(code):
    words = [word for word, in struct.iter_unpack("<I", code)]
    addresses = {word & 31 for word in words if word & 0xffc003e0 == 0x910003e0}
    loads = {(word >> 5) & 31 for word in words if word & 0xffc00000 == 0xb9400000}
    stores = {(word >> 5) & 31 for word in words if word & 0xffc00000 == 0xb9000000}
    return bool((addresses & loads & stores) - {31})


def main():
    root = Path(".local/c-pointer-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    compiler = Path(sys.argv[2]).read_bytes().strip()
    guest = Guest(workspace)
    bias = secrets.randbelow(9) + 2
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            receive(guest, b"compiler", compiler)
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            cases = [
                (
                    f"int g(int x) {{ return x*2+{bias}; }}\n"
                    "int f(int x) {\n int y=x+1; int /* alias */ *p = &y;\n"
                    " y=y+2; *p=g(*p)+x; return y+*p;\n}",
                    lambda x: 2 * (3*x + 6 + bias),
                    1,
                ),
                (
                    "int f(int x) { int y=0; int *p=&y; "
                    "while(x){ *p=*p+x; x=x-1; } return y+*p; }",
                    lambda x: x * (x+1),
                    0,
                ),
            ]
            for source, calculate, call_count in cases:
                receive(guest, b"source", source.encode())
                command(guest, b"build source", b"built\n")
                code = generated_code(guest, socket)
                if not has_stack_pointer_access(code):
                    raise ValueError("No generated load and store through a stack-derived address")
                if len(calls(code)) != call_count:
                    raise ValueError("Unexpected number of generated calls")
                for argument in (0, secrets.randbelow(7) + 1, secrets.randbelow(7) + 8):
                    command(guest, f"run {argument}".encode(), f"exit {calculate(argument):08x}\n".encode())
                if generated_code(guest, socket) != code:
                    raise ValueError("Generated code changed between runtime inputs")
            for source in (
                b"int f(int x){int y=1;return *p;}",
                b"int f(int x){int y=1;int *p=&x;return *p;}",
                b"int f(int x){int y=1;int *p=&y;return p+1;}",
            ):
                receive(guest, b"source", source)
                command(guest, b"build source", b"build error\n")
                if generated_code(guest, socket) != code:
                    raise ValueError("Rejected source replaced the previous program")
        finally:
            guest.stop()
    print(f"C pointers verified: {workspace}")


if __name__ == "__main__":
    main()
