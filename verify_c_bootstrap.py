"""Install a compiler built from C in the guest and use it to build more C."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_shell import command, read_prompt
from verify_source_import import receive


SEED_PROBE = (
    b"int score(int byte,int index,int scale,int extra){"
    b"if(byte>64){return byte+scale+extra;}return byte+index;}"
    b"int produce(char *source,int count,int *words,int capacity){"
    b"int cursor=0;int total=0;if(capacity<8){return 0;}"
    b"while(cursor<count){total=total+score(source[cursor],cursor,2,5);cursor=cursor+1;}"
    b"words[0]=4352*256*256+32+total*1024;words[1]=54879*256*256+960;return 8;}"
)


def executable(guest, socket, size_address, capacity=8192):
    length = int.from_bytes(read_memory(socket, size_address, 4, guest.run / "size.bin"), "little")
    if length < 4 or length > capacity or length % 4:
        raise ValueError(f"Invalid executable size {length}")
    return read_memory(socket, 0x40140000, length, guest.run / "executable.bin")


def main():
    root = Path(".local/c-bootstrap-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    seed, compiler = (Path(path).read_bytes().strip() for path in sys.argv[2:4])
    size_address = int(sys.argv[4], 0) if len(sys.argv) > 4 else 0x40142004
    guest = Guest(workspace)
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            receive(guest, b"seed", seed)
            receive(guest, b"compiler", compiler)
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build compiler", b"built\n")
            next_compiler = executable(guest, socket, size_address)
            command(guest, b"install", b"installed\n")
            installed = read_memory(socket, 0x40150000, len(next_compiler), guest.run / "compiler.bin")
            if installed != next_compiler:
                raise ValueError("The C-built compiler was not installed byte-for-byte")

            previous = None
            for operator in ("+", "-"):
                number = secrets.randbelow(300) + 2
                receive(guest, b"sample", f"int f(int x){{return x{operator}{number};}}".encode())
                command(guest, b"build sample", b"built\n")
                code = executable(guest, socket, size_address)
                if code == previous:
                    raise ValueError("Different C source produced identical code")
                for x in (0, secrets.randbelow(40) + 1, secrets.randbelow(900) + 100):
                    expected = x + number if operator == "+" else x - number
                    command(guest, f"run {x}".encode(), f"exit {expected & 0xffffffff:08x}\n".encode())
                if executable(guest, socket, size_address) != code:
                    raise ValueError("Generated code changed after execution")
                previous = code

            for invalid in (b"int f(int x){return x+;}", b"int f(int x){return x+4;} junk"):
                receive(guest, b"sample", invalid)
                command(guest, b"build sample", b"build error\n")
                if executable(guest, socket, size_address) != previous:
                    raise ValueError("Invalid source replaced the previous executable")
            receive(guest, b"probe", SEED_PROBE)
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build probe", b"built\n")
            command(guest, b"install", b"installed\n")
            for _ in range(2):
                payload = b"Az" + secrets.token_hex(3).encode()
                receive(guest, b"sample", payload)
                command(guest, b"build sample", b"built\n")
                score = sum(byte + (7 if byte > 64 else i) for i, byte in enumerate(payload))
                command(guest, b"run 37", f"exit {37+score:08x}\n".encode())
        finally:
            guest.stop()
    print(f"C compiler bootstrap verified: {workspace}")


if __name__ == "__main__":
    main()
