"""Compare a guest-built sbase echo with the upstream host reference."""
import hashlib
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt
from verify_source_import import receive


UPSTREAM_SHA256 = "117c10e0e5a5139a80490673a3f14dd1dfcc45856adb84a83b28e3b301f1b48c"


def install_cli(guest):
    command(guest, b"as seed", b"assembled\n")
    command(guest, b"install", b"installed\n")
    for name in (b"base", b"cli"):
        command(guest, b"build " + name, b"built\n")
        command(guest, b"install", b"installed\n")


def build_upstream(guest, name):
    install_cli(guest)
    command(guest, b"build adapter", b"built\n")
    command(guest, b"install", b"installed\n")
    command(guest, b"build " + name, b"built\n")
    guest.serial_send(b"exec adapter\n".hex())
    output = read_prompt(guest)
    suffix = b"exit 00000000\nshell> "
    if not output.endswith(suffix):
        raise ValueError(f"Adapter did not exit successfully: {output!r}")
    lines = output[:-len(suffix)].splitlines()
    if (not lines or not lines[0].startswith(b"save extra4 ") or
            any(not line.startswith(b"append extra4 ") for line in lines[1:])):
        raise ValueError(f"Unexpected adapter output: {output!r}")
    for line in lines:
        command(guest, line, b"saved\n")
    install_cli(guest)
    command(guest, b"build extra4", b"built\n")


def check_echo(guest, reference):
    words = [b"Word-" + secrets.token_hex(3).encode() for _ in range(3)]
    for args in ([], words, [b"-n"], [b"-n", *words], [words[0], b"-n", words[1]], [b"--", b"-n"]):
        expected = subprocess.run([reference, *args], capture_output=True, check=False)
        if expected.stderr:
            raise ValueError(f"Reference emitted unexpected stderr: {expected.stderr!r}")
        line = b" ".join([b"exec", b"echo", *args])
        command(guest, line, expected.stdout + f"exit {expected.returncode:08x}\n".encode())


def main():
    root = Path(".local/sbase-echo-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    seed, base, cli, adapter, upstream = (Path(name).read_bytes() for name in sys.argv[2:7])
    reference = Path(sys.argv[7]).resolve()
    if hashlib.sha256(upstream).hexdigest() != UPSTREAM_SHA256:
        raise ValueError("echo.c does not match the pinned sbase 0.1 source")
    guest = Guest(workspace)
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        for name, source in ((b"seed", seed.strip()), (b"base", base), (b"cli", cli), (b"adapter", adapter)):
            receive(guest, name, source)
        receive(guest, b"upstream", upstream)
        build_upstream(guest, b"upstream")
        if len(sys.argv) > 8:
            port = Path(sys.argv[8]).read_bytes()
            command(guest, b"cat extra4", port + b"\n")
        check_echo(guest, reference)

        changed = upstream.replace(b"putchar('\\n');", b"putchar('\\t');")
        if changed == upstream:
            raise ValueError("Could not change the upstream output terminator")
        receive(guest, b"variant", changed)
        build_upstream(guest, b"variant")
        command(guest, b"exec echo retained", b"retained\texit 00000000\n")
    finally:
        guest.stop()
    print(f"Upstream sbase echo verified: {workspace}")


if __name__ == "__main__":
    main()
