"""Exercise a saved shell image through the serial console."""
import secrets
import sys
import tempfile
from pathlib import Path
from time import monotonic

from guest_tool import Guest
from verify_http import verify as verify_http


def read_prompt(guest):
    output = bytearray()
    deadline = monotonic() + 5
    while monotonic() < deadline and not output.endswith(b"shell> "):
        output.extend(bytes.fromhex(guest.serial_read(250)["hex"]))
    if not output.endswith(b"shell> "):
        raise ValueError(f"No shell prompt after {bytes(output)!r}")
    return bytes(output)


def command(guest, line, expected):
    if guest.serial_send((line + b"\n").hex())["sent"] != len(line) + 1:
        raise ValueError("Incomplete serial input")
    output = read_prompt(guest)
    # A shell may echo the input line, with either LF or CRLF.
    result = output.removeprefix(line + b"\r\n").removeprefix(line + b"\n")
    if result != expected + b"shell> ":
        raise ValueError(f"Unexpected response to {line!r}: {output!r}")


def main():
    root = Path(".local/shell-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    for network in (False, True):
        guest.boot(network=network, http=network)
        try:
            output = read_prompt(guest)
            if not output.startswith(b"BOOT\n"):
                raise ValueError(f"No boot banner: {output!r}")
            nonce = b"observer " + secrets.token_hex(4).encode()
            command(guest, b"help", b"help echo\n")
            command(guest, b"echo " + nonce, nonce + b"\n")
            command(guest, b"not-a-command", b"unknown command\n")
            for _ in range(4):
                guest.serial_send((b"x" * 256).hex())
            guest.serial_send("0a")
            read_prompt(guest)
            command(guest, b"help", b"help echo\n")
        finally:
            guest.stop()
        if network and not verify_http(guest.run):
            return 1
        print(f"Shell verified: {guest.run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
