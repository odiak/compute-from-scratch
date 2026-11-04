"""Exercise isolated descriptors and offsets in two cooperative processes."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_c_subset import put_file
from verify_shell import command, read_prompt


def application(name):
    word = int.from_bytes(name.ljust(4, b"\0"), "little")
    return (
        "sub sp,sp,64;str x30,[sp];str x2,[sp,8];str x3,[sp,16];str w1,[sp,24];"
        "adr x1,name;mov w2,2;mov w0,1;ldr x9,[sp,16];blr x9;cmp w0,3;b.ne fail;"
        "adr x1,name;mov w2,2;mov w0,1;ldr x9,[sp,16];blr x9;cmp w0,4;b.ne fail;"
        "mov w0,2;mov w1,3;add x2,sp,32;mov w3,1;ldr x9,[sp,16];blr x9;cmp w0,1;b.ne fail;"
        "mov w0,3;mov w1,1;add x2,sp,32;mov w3,1;ldr x9,[sp,16];blr x9;cmp w0,1;b.ne fail;"
        "ldr x9,[sp,8];blr x9;"
        "mov w0,2;mov w1,3;add x2,sp,32;mov w3,8;ldr x9,[sp,16];blr x9;cmp w0,2;b.ne fail;"
        "mov w0,3;mov w1,1;add x2,sp,32;mov w3,2;ldr x9,[sp,16];blr x9;cmp w0,2;b.ne fail;"
        "mov w0,2;mov w1,3;add x2,sp,32;mov w3,1;ldr x9,[sp,16];blr x9;cmp w0,0;b.ne fail;"
        "mov w0,4;mov w1,3;ldr x9,[sp,16];blr x9;cmp w0,0;b.ne fail;"
        "mov w0,2;mov w1,4;add x2,sp,32;mov w3,1;ldr x9,[sp,16];blr x9;cmp w0,1;b.ne fail;"
        "ldr w0,[sp,24];b done;fail:;mov w0,0;done:;ldr x30,[sp];add sp,sp,64;ret;"
        f"name:;.word {word}"
    ).encode()


def main():
    root = Path(".local/process-io-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    first = bytes(65 + secrets.randbelow(13) for _ in range(3))
    second = bytes(110 + secrets.randbelow(13) for _ in range(3))
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        for i, data in enumerate((first, second), 1):
            name = f"f{i}".encode()
            put_file(guest, name, data)
            put_file(guest, b"test", application(name))
            command(guest, b"as test", b"assembled\n")
            command(guest, f"spawn {i+10}".encode(), f"pid {i}\n".encode())
        guest.serial_send(b"schedule\n".hex())
        output = read_prompt(guest)
        if first[:1] + second[:1] + first[1:] + second[1:] not in output:
            raise ValueError(f"Process file output did not interleave: {output!r}")
        command(guest, b"wait 1", b"exit 0000000b\n")
        command(guest, b"wait 2", b"exit 0000000c\n")
        command(guest, b"spawn 13", b"pid 1\n")
        guest.serial_send(b"schedule\n".hex())
        if second not in read_prompt(guest):
            raise ValueError("Reused process did not start with fresh descriptors")
        command(guest, b"wait 1", b"exit 0000000d\n")
    finally:
        guest.stop()
    print(f"Process I/O verified: {workspace}")


if __name__ == "__main__":
    main()
