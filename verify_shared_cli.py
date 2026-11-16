"""Verify stage039 from saved source, shared libc and pinned host references.

Usage: verify_shared_cli.py IMAGE ECHO_REFERENCE CAT_REFERENCE BASENAME_REFERENCE [ARTIFACTS_DIR]
"""
import hashlib
import json
import os
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_bootstrap import executable
from verify_sbase_echo import check_echo
from verify_shell import command, read_prompt
from verify_source_import import receive


SOURCES = {
    "new1": "experiments/032-seed.s",
    "extra1": "experiments/034-compiler.c",
    "extra3": "experiments/035-compiler.c",
    "raw": "experiments/039-bootstrap-compiler.c",
    "extra2": "experiments/039-compiler.c",
    "libc": "experiments/039-libc.c",
    "stdioh": "experiments/039-stdio.h",
    "stringh": "experiments/039-string.h",
    "utilh": "experiments/039-util.h",
    "fcntlh": "experiments/039-fcntl.h",
    "libgenh": "experiments/039-libgen.h",
    "unistdh": "experiments/039-unistd.h",
    "Abc123xyz789": "fixtures/sbase-0.1/arg.h",
    "alpha": "fixtures/sbase-0.1/cat.c",
    "beta": "fixtures/sbase-0.1/basename.c",
    "extra5": "fixtures/sbase-0.1/echo.c",
    "catbuild": "experiments/039-cat-build.c",
    "basebuild": "experiments/039-basename-build.c",
    "Check": "experiments/039-echo-build.c",
}
CAPACITY = 65532


def bootstrap(guest):
    command(guest, b"as new1", b"assembled\n")
    command(guest, b"install", b"installed\n")
    for name in (b"extra1", b"extra3", b"raw"):
        command(guest, b"build " + name, b"built\n")
        command(guest, b"install", b"installed\n")


def main():
    image = Path(sys.argv[1])
    references = dict(zip(("echo", "cat", "basename"), (Path(p).resolve() for p in sys.argv[2:5])))
    artifacts = Path(sys.argv[5]) if len(sys.argv) > 5 else Path("experiments")
    root = Path(".local/shared-cli-check")
    root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=root)).resolve()
    (work / "guest.hex").write_bytes(image.read_bytes())
    reference_dir = work / "reference"
    reference_dir.mkdir()
    sources = {}
    for name, path in SOURCES.items():
        source = Path(path)
        if source.name.startswith("039-"):
            source = artifacts / source.name
        sources[name.encode()] = source.read_bytes()
    pins = json.loads(Path("fixtures/sbase-0.1/manifest.json").read_text())["files"]
    for name in ("echo.c", "cat.c", "basename.c", "arg.h"):
        source = Path("fixtures/sbase-0.1", name).read_bytes()
        if hashlib.sha256(source).hexdigest() != pins[name]["sha256"]:
            raise ValueError(f"Pinned upstream input changed: {name}")
    guest = Guest(work)

    def compare(program, args, guest_args=None, stdin=b""):
        expected = subprocess.run(
            [program, *args], executable=str(references[program]), input=stdin,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=reference_dir,
            env={**os.environ, "LC_ALL": "C"}, check=False,
        )
        line = " ".join(["exec", program, *(args if guest_args is None else guest_args)])
        command(guest, line.encode(), expected.stdout + f"exit {expected.returncode:08x}\n".encode())
        return expected

    with tempfile.TemporaryDirectory(dir="/tmp") as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            for name, source in sources.items():
                receive(guest, name, source)
            bootstrap(guest)
            generations = []
            for index in range(3):
                command(guest, b"build extra2", b"built\n")
                code = executable(guest, socket, 0x41100004, CAPACITY)
                (work / f"generation-{index}.bin").write_bytes(code)
                command(guest, b"install", b"installed\n")
                installed = read_memory(socket, 0x40150000, len(code), work / "installed.bin")
                if code != installed:
                    raise ValueError("Installed compiler differs from generated code")
                generations.append(code)
            if generations[1] != generations[2]:
                raise ValueError("Successive compiler self-builds differ")

            for fixture in ("preprocessor.c", "semantics.c"):
                receive(guest, b"probe", Path("fixtures/c-native", fixture).read_bytes())
                command(guest, b"build probe", b"built\n")
                command(guest, b"exec Probe runtime", b"exit 00000000\n")
            command(guest, b"build Check", b"built\n")
            check_echo(guest, references["echo"])
            command(guest, b"build basebuild", b"built\n")
            for args in (["/dir/thing.c", ".c"], ["/"], ["////"], ["thing///"],
                         ["foo", "foo"], ["--", "-name"], [], ["-z"], ["a", "b", "c"]):
                compare("basename", args)

            first, second, input_name, made = (prefix + secrets.token_hex(3) for prefix in "fsip")
            first_data = b"A\x00\x04B-" + secrets.token_bytes(12) + b"\n"
            second_data = b"Last-" + secrets.token_hex(4).encode() + b"\n"
            input_data = b"Input-" + secrets.token_hex(4).encode() + b"\n"
            for name, data in ((first, first_data), (second, second_data), (input_name, input_data)):
                receive(guest, name.encode(), data)
                (reference_dir / name).write_bytes(data)
            command(guest, b"build catbuild", b"built\n")
            compare("cat", [first])
            compare("cat", [first, second])
            compare("cat", ["-u", first])
            compare("cat", ["-u", "--", first])
            compare("cat", [], ["<", input_name], input_data)
            compare("cat", [first, "-", second], ["<", input_name, first, "-", second], input_data)
            compare("cat", ["-", "-"], ["<", input_name, "-", "-"], input_data)
            missing = "m" + secrets.token_hex(4)
            compare("cat", [missing, second])
            compare("cat", ["-z"])
            receive(guest, input_name.encode(), b"")
            compare("cat", [], ["<", input_name])
            before = executable(guest, socket, 0x41100004, CAPACITY)
            receive(guest, b"probe", b"int main(){return 1+;}")
            command(guest, b"build probe", b"build error\n")
            if executable(guest, socket, 0x41100004, CAPACITY) != before:
                raise ValueError("Failed compilation changed the previous executable")
            compare("cat", [first])

            receive(guest, b"probe", Path("fixtures/c-native/file-io.c").read_bytes())
            command(guest, b"build probe", b"built\n")
            command(guest, f"exec FileIO {made} {'0' * 40}".encode(), b"A\x00Z\nexit 00000000\n")
            command(guest, b"build catbuild", b"built\n")
            command(guest, f"exec cat 2> {first} {missing}".encode(), b"exit 00000001\n")
            expected_error = subprocess.run(
                ["cat", missing], executable=str(references["cat"]), capture_output=True,
                cwd=reference_dir, env={**os.environ, "LC_ALL": "C"}, check=False,
            ).stderr
            command(guest, b"cat " + first.encode(), expected_error + b"\n")
            command(guest, b"build basebuild", b"built\n")
            command(guest, f"exec basename > {second} /dir/thing.c .c".encode(), b"exit 00000000\n")
            command(guest, b"cat " + second.encode(), b"thing\n\n")
            command(guest, b"build catbuild", b"built\n")
            console = b"Console-" + secrets.token_hex(5).encode() + b"\n"
            guest.serial_send((b"exec cat\n" + console + b"\x04").hex())
            if read_prompt(guest) != console + b"exit 00000000\nshell> ":
                raise ValueError("Console stdin/EOF differs from supplied input")

            guest.stop()
            guest.boot(disk=True)
            read_prompt(guest)
            command(guest, b"cat " + made.encode(), b"A\x00Z\n\n")
            for name, source in sources.items():
                command(guest, b"cat " + name, source + b"\n")
            bootstrap(guest)
            command(guest, b"build extra2", b"built\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build Check", b"built\n")
            check_echo(guest, references["echo"])
            command(guest, b"build catbuild", b"built\n")
            command(guest, b"exec cat " + made.encode(), b"A\x00Z\nexit 00000000\n")
        finally:
            guest.stop()
    print(f"Shared upstream CLI verified: sizes={list(map(len, generations))}, "
          f"sha256={hashlib.sha256(generations[-1]).hexdigest()}, {work}")


if __name__ == "__main__":
    main()
