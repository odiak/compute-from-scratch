"""Compile and execute C functions through the guest-only toolchain."""
import secrets
import struct
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_subset import put_file
from verify_shell import command, read_prompt


def generated_code(guest, socket):
    size = int.from_bytes(read_memory(socket, 0x40142004, 4, guest.run / "size.bin"), "little")
    if not 4 <= size <= 2048 or size % 4:
        raise ValueError(f"Unexpected generated length: {size}")
    return read_memory(socket, 0x40140000, size, guest.run / "compiled.bin")


def calls(code):
    words = [word for word, in struct.iter_unpack("<I", code)]
    targets = []
    for index, word in enumerate(words):
        if word >> 26 == 0b100101:
            delta = (word & 0x1ffffff) - (word & 0x2000000)
            target = index + delta
            if target == index or not 0 <= target < len(words):
                raise ValueError("BL does not target a different generated instruction")
            targets.append(target)
    return targets


def main():
    root = Path(".local/c-functions-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    compiler = Path(sys.argv[2]).read_bytes().strip()
    guest = Guest(workspace)
    scale, bias = (secrets.randbelow(12) + 2 for _ in range(2))
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            put_file(guest, b"compiler", compiler)
            command(guest, b"as compiler", b"assembled\n")
            command(guest, b"install", b"installed\n")
            prefix = f"int g(int x){{return x*{scale}+{bias};}} "
            programs = [
                ("int f(int x){int y=x+1;y=g(y)+g(x+2);return y+x;}",
                 lambda x: scale * (2*x + 3) + 2*bias + x, 2),
                ("int f(int x){int y=0;while(x){y=y+g(x);x=x-1;}return y;}",
                 lambda x: scale*x*(x+1)//2 + bias*x, 1),
            ]
            for source, expected, count in programs:
                put_file(guest, b"test", (prefix + source).encode())
                command(guest, b"build test", b"built\n")
                code = generated_code(guest, socket)
                targets = calls(code)
                if len(targets) != count or len(set(targets)) != 1:
                    raise ValueError(f"Expected {count} BL instructions to one helper, got {targets}")
                for argument in (0, secrets.randbelow(6) + 1, secrets.randbelow(8) + 7):
                    command(guest, f"run {argument}".encode(), f"exit {expected(argument):08x}\n".encode())
                if generated_code(guest, socket) != code:
                    raise ValueError("Generated code changed between runtime inputs")
            put_file(guest, b"test", (prefix + "int f(int x){return g(x,1);}").encode())
            command(guest, b"build test", b"build error\n")
            if generated_code(guest, socket) != code:
                raise ValueError("Failed compilation replaced the previous executable")
        finally:
            guest.stop()
    print(f"C functions verified: {workspace}")


if __name__ == "__main__":
    main()
