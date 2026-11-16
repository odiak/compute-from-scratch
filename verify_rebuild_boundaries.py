"""Check stage041 batch validation and failed executable-load preservation."""
import shutil
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_development import enter, until
from verify_environment_rebuild import code, files
from verify_shell import read_prompt
from verify_source_import import receive


def main():
    source = Path(sys.argv[1])
    root = Path(".local/rebuild-boundary-check")
    root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=root)).resolve()
    for name in ("guest.hex", "disk.img"):
        shutil.copyfile(source / name, work / name)
    saved = files((source / "disk.img").read_bytes())
    resident = code(saved, "devbin")
    compiler = code(saved, "ccbin")
    guest = Guest(work)

    def load():
        guest.serial_send(b"enter devbin devbin.2 dev restore ccbin ccbin.2\n".hex())
        until(guest, b"dev> ")

    def leave():
        enter(guest, b"quit", b"shell> ")

    with tempfile.TemporaryDirectory() as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            load()
            assert read_memory(socket, 0x40150000, len(compiler), work / "loaded-compiler.bin") == compiler
            leave()
            assert read_memory(socket, 0x40150000, len(compiler), work / "returned-compiler.bin") == compiler, \
                "Returning from loaded development shell changed the installed compiler"
            guest.serial_send(b"enter devbin devbin.2 dev\n".hex())
            until(guest, b"dev> ")
            enter(guest, b"build extra2", contains=b"built\nstatus 0\n")
            assert read_memory(socket, 0x40c00000, len(compiler), work / "rebuilt-compiler.bin") == compiler
            enter(guest, b"edit exitcase", b"edit> ")
            enter(guest, b'i 1 #include "libc"', b"edit> ")
            enter(guest, b'i 2 int main(void){out(2,"nested-exit\\n");exit(7);return 0;}', b"edit> ")
            enter(guest, b"w", b"edit> ", b"saved\n")
            enter(guest, b"q", contains=b"status 0\n")
            enter(guest, b"build exitcase", contains=b"built\nstatus 0\n")
            enter(guest, b"save exitcase -", contains=b"status 0\n")
            leave()
            guest.serial_send(b"enter exitcase - chosen\n".hex())
            response = read_prompt(guest)
            assert b"nested-exit\n" in response
            assert read_memory(socket, 0x40150000, len(compiler), work / "exit-compiler.bin") == compiler
            load()
            enter(guest, b"remove exitcase", contains=b"status 0\n")
            leave()
            cases = (
                ((5).to_bytes(4, "little") + b"\0" * 5, "scratch"),
                ((65536).to_bytes(4, "little") + b"\0" * 4, "scratch"),
                ((8).to_bytes(4, "little") + b"\0" * 4, "scratch"),
                ((8).to_bytes(4, "little") + b"\0" * 12, "scratch"),
                ((32768).to_bytes(4, "little") + b"\0" * 32764, "absent"),
            )
            for index, (data, second) in enumerate(cases):
                receive(guest, b"scratch", data)
                # The resident C image contains mutable library globals.
                before = read_memory(socket, 0x40140000, len(resident), work / "before.bin")
                guest.serial_send(f"enter scratch {second} dev\n".encode().hex())
                response = read_prompt(guest)
                assert b"?\n" in response, (index, repr(response[:200]))
                assert read_memory(socket, 0x40140000, len(resident), work / "resident.bin") == before
                assert read_memory(socket, 0x40150000, len(compiler), work / "compiler.bin") == compiler
                load()
                enter(guest, b"@echo recovered", contains=b"recovered\nstatus 0\n")
                leave()

            for data in (b"echo should-not-run", b"echo should-not-run\0\n", b"x" * 127 + b"\n"):
                receive(guest, b"scratch", data)
                guest.serial_send(b"batch scratch\n".hex())
                response = read_prompt(guest)
                assert b"?\n" in response and b"should-not-run" not in response
                assert b"unknown command" not in response
                guest.serial_send(b"echo recovered\n".hex())
                until(guest, b"recovered\nshell> ")
        finally:
            guest.stop()
    print(f"Batch and executable-load boundaries verified: {work}")


if __name__ == "__main__":
    main()
