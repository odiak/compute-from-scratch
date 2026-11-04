"""Bootstrap a guest C compiler and compare two successive self-builds."""
import hashlib
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_bootstrap import executable
from verify_shell import command, read_prompt
from verify_source_import import receive


def main():
    root = Path(".local/self-compiler-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    seed = Path(sys.argv[2]).read_bytes().strip()
    source = Path(sys.argv[3]).read_bytes()
    guest = Guest(workspace)
    bias = secrets.randbelow(20) + 2
    helper = "step" + secrets.token_hex(2)
    test = (
        f"int {helper}(int n,int k){{return n*2+k;}}"
        "int evaluate(int n){int sum=0;"
        f"while(n>0){{sum=sum+{helper}(n,{bias});n=n-1;}}"
        "return sum;}"
    ).encode()
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            receive(guest, b"seed", seed)
            receive(guest, b"compiler", source)
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            generations = []
            for index in range(3):
                command(guest, b"build compiler", b"built\n")
                code = executable(guest, socket, 0x41100004, capacity=32768)
                generations.append(code)
                (guest.run / f"generation-{index}.bin").write_bytes(code)
                command(guest, b"install", b"installed\n")
                installed = read_memory(socket, 0x40150000, len(code), guest.run / "installed.bin")
                if installed != code:
                    raise ValueError(f"Generation {index} was not installed byte-for-byte")
            if generations[1] != generations[2]:
                raise ValueError("The two self-built compiler generations differ")

            receive(guest, b"sample", test)
            command(guest, b"build sample", b"built\n")
            code = executable(guest, socket, 0x41100004, capacity=32768)
            for n in (0, secrets.randbelow(8) + 1, secrets.randbelow(12) + 9):
                expected = n*(n+1) + n*bias
                command(guest, f"run {n}".encode(), f"exit {expected:08x}\n".encode())

            receive(guest, b"sample", b"int broken(int n){return n+;}")
            command(guest, b"build sample", b"build error\n")
            if executable(guest, socket, 0x41100004, capacity=32768) != code:
                raise ValueError("The failed build replaced the previous executable")
        finally:
            guest.stop()
    sizes = [len(code) for code in generations]
    print(f"C compiler self-host verified: sizes={sizes}, "
          f"sha256={hashlib.sha256(generations[2]).hexdigest()}, {workspace}")


if __name__ == "__main__":
    main()
