"""Bootstrap the stage038 compiler and build unmodified upstream echo in the guest."""
import hashlib
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_bootstrap import executable
from verify_sbase_echo import UPSTREAM_SHA256, check_echo
from verify_shell import command, read_prompt
from verify_source_import import receive


def main():
    root = Path(".local/native-echo-check")
    root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=root)).resolve()
    image, bridge, compiler, stdio, string, util, reference = map(Path, sys.argv[1:8])
    (work / "guest.hex").write_bytes(image.read_bytes())
    upstream = Path("fixtures/sbase-0.1/echo.c").read_bytes()
    assert hashlib.sha256(upstream).hexdigest() == UPSTREAM_SHA256
    sources = {
        b"seed": Path("experiments/032-seed.s").read_bytes(),
        b"base": Path("experiments/034-compiler.c").read_bytes(),
        b"cli": Path("experiments/035-compiler.c").read_bytes(),
        b"bridge": bridge.read_bytes(), b"compiler": compiler.read_bytes(),
        b"stdioh": stdio.read_bytes(), b"stringh": string.read_bytes(),
        b"utilh": util.read_bytes(), b"upstream": upstream,
    }
    guest = Guest(work)
    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            for name, source in sources.items():
                receive(guest, name, source)
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            for name in (b"base", b"cli", b"bridge"):
                command(guest, b"build " + name, b"built\n")
                command(guest, b"install", b"installed\n")
            generations = []
            for index in range(3):
                command(guest, b"build compiler", b"built\n")
                code = executable(guest, socket, 0x41100004, capacity=60000)
                (work / f"generation-{index}.bin").write_bytes(code)
                command(guest, b"install", b"installed\n")
                assert read_memory(socket, 0x40150000, len(code), work / "installed.bin") == code
                generations.append(code)
            assert generations[1] == generations[2]

            receive(guest, b"semantics", Path("fixtures/c-native/semantics.c").read_bytes())
            command(guest, b"build semantics", b"built\n")
            command(guest, b"exec Probe", b"exit 00000000\n")
            command(guest, b"exec Probe " + secrets.token_hex(5).encode(), b"exit 00000000\n")

            command(guest, b"build upstream", b"built\n")
            check_echo(guest, reference.resolve())
            code = executable(guest, socket, 0x41100004, capacity=60000)
            receive(guest, b"invalid", b"int main(){return 1+;}")
            command(guest, b"build invalid", b"build error\n")
            assert executable(guest, socket, 0x41100004, capacity=60000) == code
            check_echo(guest, reference.resolve())
            changed = upstream.replace(b"putchar('\\n');", b"putchar('\\t');")
            assert changed != upstream
            receive(guest, b"variant", changed)
            command(guest, b"build variant", b"built\n")
            word = secrets.token_hex(5).encode()
            command(guest, b"exec Variant " + word, word + b"\texit 00000000\n")
            command(guest, b"exec Variant -n " + word, word + b"exit 00000000\n")
            command(guest, b"cat upstream", upstream + b"\n")
            guest.stop()

            guest.boot(disk=True)
            read_prompt(guest)
            for name, source in sources.items():
                command(guest, b"cat " + name, source + b"\n")
            command(guest, b"as seed", b"assembled\n")
            command(guest, b"install", b"installed\n")
            for name in (b"base", b"cli", b"bridge", b"compiler"):
                command(guest, b"build " + name, b"built\n")
                command(guest, b"install", b"installed\n")
            command(guest, b"build upstream", b"built\n")
            check_echo(guest, reference.resolve())
        finally:
            guest.stop()
    print(f"Native upstream echo verified: sizes={list(map(len, generations))}, "
          f"sha256={hashlib.sha256(generations[-1]).hexdigest()}, {work}")


if __name__ == "__main__":
    main()
