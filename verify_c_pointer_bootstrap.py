"""Verify the intermediate stage038 pointer compiler, not native echo acceptance."""
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
    root = Path(".local/c-pointer-bootstrap-check")
    root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=root)).resolve()
    (work / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    sources = [Path(path).read_bytes() for path in sys.argv[2:6]]
    guest = Guest(work)
    word = ("K" + secrets.token_hex(4)).encode()
    probe = (
        b"int main(int argc,char **argv){char **p=1+argv;"
        b"if(p-argv-1){return 93;}if(argc>1){putchar(**p);}return argc;}"
    )
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            for name, source in zip((b"seed", b"base", b"cli", b"compiler"), sources):
                receive(guest, name, source)
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            for name in (b"base", b"cli"):
                command(guest, b"build " + name, b"built\n")
                command(guest, b"install", b"installed\n")
            generations = []
            for index in range(3):
                command(guest, b"build compiler", b"built\n")
                code = executable(guest, socket, 0x41100004, capacity=32768)
                (work / f"generation-{index}.bin").write_bytes(code)
                command(guest, b"install", b"installed\n")
                assert read_memory(socket, 0x40150000, len(code), work / "installed.bin") == code
                generations.append(code)
            assert generations[1] == generations[2]
            receive(guest, b"probe", probe)
            command(guest, b"build probe", b"built\n")
            code = executable(guest, socket, 0x41100004, capacity=32768)
            command(guest, b"exec Probe " + word, word[:1] + b"exit 00000002\n")
            command(guest, b"exec Probe", b"exit 00000001\n")
            receive(guest, b"probe", b"int main(){return 1+;}")
            command(guest, b"build probe", b"build error\n")
            assert executable(guest, socket, 0x41100004, capacity=32768) == code
            command(guest, b"exec Probe " + word, word[:1] + b"exit 00000002\n")
        finally:
            guest.stop()
    print(f"Intermediate pointer bootstrap verified: sizes={list(map(len, generations))}, "
          f"sha256={hashlib.sha256(generations[-1]).hexdigest()}, {work}")


if __name__ == "__main__":
    main()
