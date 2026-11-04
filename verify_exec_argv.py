"""Check that guest applications receive a real argc/argv across console calls."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_shell import command, read_prompt
from verify_source_import import receive


PROBE = (
    "sub sp,sp,64;str x19,[sp];str x20,[sp,8];str x21,[sp,16];"
    "str x22,[sp,24];str x23,[sp,32];str x24,[sp,40];str x30,[sp,48];"
    "mov x19,x0;mov x20,x2;mov w22,w1;mov w24,w1;mov w23,0;"
    "arg:;cmp w24,0;b.eq end;ldr x21,[x20];cmp w21,0;b.eq bad;"
    "mov w0,91;blr x19;"
    "char:;ldrb w0,[x21];cmp w0,0;b.eq close;add w23,w23,w0;"
    "blr x19;add x21,x21,1;b char;"
    "close:;mov w0,93;blr x19;add x20,x20,8;sub w24,w24,1;b arg;"
    "end:;ldr w21,[x20];cmp w21,0;b.ne bad;ldr w21,[x20,4];cmp w21,0;b.ne bad;"
    "mov w0,10;blr x19;add w0,w23,w22;b out;bad:;mov w0,65535;"
    "out:;ldr x30,[sp,48];ldr x24,[sp,40];ldr x23,[sp,32];ldr x22,[sp,24];"
    "ldr x21,[sp,16];ldr x20,[sp,8];ldr x19,[sp];add sp,sp,64;ret;"
).encode()


def main():
    root = Path(".local/argv-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_bytes(Path(sys.argv[1]).read_bytes())
    guest = Guest(workspace)
    token = secrets.token_hex(5).encode()
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        command(guest, b"exec unloaded", b"invalid exec\n")
        receive(guest, b"probe", PROBE)
        command(guest, b"as probe", b"assembled\n")
        for args in (
            [b"test-" + token],
            [b"Test", b"-n", token, b"LAST"],
            [b"test", b"A1", b"Z", token, b"0", b"--", b"seventh", b"8th"],
        ):
            checksum = sum(map(sum, args)) + len(args)
            output = b"".join(b"[" + arg + b"]" for arg in args)
            command(guest, b"exec  " + b"   ".join(args), output + f"\nexit {checksum:08x}\n".encode())
        for bad in (b"exec", b"exec   ", b"exec " + b" ".join([b"a"] * 48)):
            command(guest, bad, b"invalid exec\n")
        command(guest, b"exec A", b"[A]\nexit 00000042\n")

        receive(guest, b"legacy", b"mov w0,w1;ret;")
        command(guest, b"as legacy", b"assembled\n")
        command(guest, b"run 123456", b"exit 0001e240\n")
        command(guest, b"echo alive", b"alive\n")
    finally:
        guest.stop()
    print(f"Exec argv verified: {workspace}")


if __name__ == "__main__":
    main()
