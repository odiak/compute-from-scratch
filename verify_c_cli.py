"""Rebuild the extended guest compiler and exercise its C CLI runtime."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_c_bootstrap import executable
from verify_shell import command, read_prompt
from verify_source_import import receive


def main():
    root = Path(".local/c-cli-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    seed, base, compiler, runtime = (Path(name).read_bytes() for name in sys.argv[2:6])
    guest = Guest(workspace)
    key = "Key" + secrets.token_hex(4)
    probe = (
        "int main(int count,char **arguments){int status=0;"
        "if(arguments[count]){return 99;}"
        "if(count<2){status=puts(\"NO ARG\");return 2;}"
        f"if(strcmp(arguments[1],\"{key}\"))"
        "{status=puts(\"different\");return 3;}"
        "status=puts(\"same\\nvalue\");"
        "status=putchar('!');status=putchar('\\n');"
        "status=puts(arguments[1]);return 7;}"
    ).encode()
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            for name, data in ((b"seed", seed.strip()), (b"base", base), (b"compiler", compiler)):
                receive(guest, name, data)
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build base", b"built\n")
            command(guest, b"install", b"installed\n")
            previous = None
            for index in range(3):
                command(guest, b"build compiler", b"built\n")
                code = executable(guest, socket, 0x41100004, capacity=32768)
                if index == 2 and previous != code:
                    raise ValueError("Extended compiler self-builds produced different code")
                command(guest, b"install", b"installed\n")
                previous = code

            receive(guest, b"probe", runtime + b"\n" + probe)
            command(guest, b"build probe", b"built\n")
            command(guest, b"exec Demo", b"NO ARG\nexit 00000002\n")
            command(guest, b"exec Demo " + key.swapcase().encode(), b"different\nexit 00000003\n")
            output = b"same\nvalue\n!\n" + key.encode() + b"\nexit 00000007\n"
            command(guest, b"exec Demo " + key.encode() + b" Extra", output)
        finally:
            guest.stop()
    print(f"C CLI runtime verified: {workspace}")


if __name__ == "__main__":
    main()
