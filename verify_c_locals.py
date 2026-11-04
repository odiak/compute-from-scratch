"""Verify named locals and independently named parameters in the guest compiler."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_c_functions import calls, generated_code
from verify_shell import command, read_prompt
from verify_source_import import receive


def main():
    root = Path(".local/c-locals-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    compiler = Path(sys.argv[2]).read_bytes().strip()
    guest = Guest(workspace)
    bias = secrets.randbelow(17) + 2
    name = "val" + secrets.token_hex(2)
    count, upper, result = name + "_size", name.upper(), "_" + name + "_r2"
    source = (
        f"int g(int _input){{return _input*2+{bias};}}\n"
        "int f(int index9){\n"
        f"int {name}=index9+1; int {count}={name}+g(index9);\n"
        f"int {upper}={count}-{name}; int {result}=g({upper})+{count};\n"
        f"while(index9){{{name}={name}+{upper};index9=index9-1;}}\n"
        f"if({upper}){{{result}={result}+{name};}}\n"
        f"return {result}-{count}+{name};}}"
    )
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            receive(guest, b"compiler", compiler)
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            receive(guest, b"source", source.encode())
            command(guest, b"build source", b"built\n")
            code = generated_code(guest, socket)
            if len(calls(code)) != 2:
                raise ValueError("Expected two generated calls to the helper")
            for x in (0, secrets.randbelow(9) + 1, secrets.randbelow(11) + 10):
                delta = 2*x + bias
                total = x + 1 + x*delta
                expected = 2*delta + bias + 2*total
                command(guest, f"run {x}".encode(), f"exit {expected:08x}\n".encode())
            if generated_code(guest, socket) != code:
                raise ValueError("Generated code changed between runtime inputs")

            for invalid in (
                b"int f(int input){int total=1;int total=2;return total;}",
                b"int f(int input){int input=2;return input;}",
                b"int f(int input){int total=1;return tota;}",
                b"int f(int input){int 1value=0;return input;}",
                b"int f(int input){int if=0;return input;}",
                b"int g(int first){return second;} int f(int second){return g(second);}",
            ):
                receive(guest, b"source", invalid)
                command(guest, b"build source", b"build error\n")
                if generated_code(guest, socket) != code:
                    raise ValueError("Rejected source replaced the previous program")
        finally:
            guest.stop()
    print(f"C named locals verified: {workspace}")


if __name__ == "__main__":
    main()
