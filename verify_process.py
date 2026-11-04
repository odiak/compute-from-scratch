"""Verify separate process images, stack state, cooperative scheduling, and wait."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_c_subset import put_file
from verify_shell import command, read_prompt


def application(delta):
    return (
        "sub sp,sp,32;str x30,[sp];str x0,[sp,8];str x2,[sp,16];str w1,[sp,24];"
        "mov w0,w1;ldr x3,[sp,8];blr x3;ldr x3,[sp,16];blr x3;"
        "ldr w0,[sp,24];add w0,w0,32;ldr x3,[sp,8];blr x3;"
        f"ldr w0,[sp,24];add w0,w0,{delta};ldr x30,[sp];add sp,sp,32;ret"
    ).encode()


def main():
    root = Path(".local/process-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    codes = [65 + secrets.randbelow(12), 78 + secrets.randbelow(12)]
    deltas = [100 + secrets.randbelow(100), 300 + secrets.randbelow(100)]
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        for i, (code, delta) in enumerate(zip(codes, deltas), 1):
            put_file(guest, b"test", application(delta))
            command(guest, b"as test", b"assembled\n")
            command(guest, f"spawn {code}".encode(), f"pid {i}\n".encode())
        guest.serial_send(b"schedule\n".hex())
        output = read_prompt(guest)
        expected = bytes(codes + [code + 32 for code in codes])
        if expected not in output:
            raise ValueError(f"Process output did not interleave: {output!r}")
        for i, (code, delta) in enumerate(zip(codes, deltas), 1):
            command(guest, f"wait {i}".encode(), f"exit {code+delta:08x}\n".encode())
        command(guest, f"spawn {codes[0]}".encode(), b"pid 1\n")
        guest.serial_send(b"schedule\n".hex())
        if bytes([codes[0], codes[0]+32]) not in read_prompt(guest):
            raise ValueError("Reused slot did not resume across yield")
        command(guest, b"wait 1", f"exit {codes[0]+deltas[1]:08x}\n".encode())
    finally:
        guest.stop()
    print(f"Processes verified: {workspace}")


if __name__ == "__main__":
    main()
