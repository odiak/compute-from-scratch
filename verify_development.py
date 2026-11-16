"""Independently rebuild and exercise the stage040 guest development shell."""
import hashlib
import json
import secrets
import sys
import tempfile
from pathlib import Path
from time import monotonic

from guest_tool import Guest
from observer_qmp import read_memory
from verify_c_bootstrap import executable
from verify_shared_cli import SOURCES, bootstrap
from verify_shell import command, read_prompt
from verify_source_import import receive


def until(guest, prompt, timeout=15):
    data = bytearray()
    deadline = monotonic() + timeout
    while monotonic() < deadline:
        data.extend(bytes.fromhex(guest.serial_read(100)["hex"]))
        if data.endswith(prompt):
            return bytes(data)
    raise ValueError(f"Missing {prompt!r}: {len(data)} output bytes; "
                     f"first={bytes(data[:200])!r}, last={bytes(data[-200:])!r}")


def enter(guest, line, prompt=b"dev> ", contains=None):
    guest.serial_send((line + b"\n").hex())
    output = until(guest, prompt)
    result = output.removeprefix(line + b"\n").removeprefix(line + b"\r\n")
    if contains is not None and contains not in result:
        raise ValueError(f"{line!r}: expected {contains!r}, got {output!r}")
    return result


def main():
    snapshot = Path(sys.argv[1])
    root = Path(".local/development-check")
    root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=root)).resolve()
    (work / "guest.hex").write_bytes((snapshot / "guest.hex").read_bytes())
    inputs = {name: (snapshot / "files" / name).read_bytes() for name in SOURCES}
    inputs["extra4"] = (snapshot / "files/extra4").read_bytes()
    marker = "Independent-" + secrets.token_hex(4)
    source = [
        '#include "libc"',
        'int main(int ac,char **av){',
        'int n=0;char *b=(char *)(16624*256*256+1024*256);',
        'if(ac<2){puts("' + marker + '");return 0;}',
        'if(!strcmp(av[1],"exit")){out(2,"nested exit\\n");exit(7);}',
        'if(!strcmp(av[1],"emit")){n=0;while(n<32768){b[n]=97;n++;}return write(1,b,n)!=n;}',
        'while((n=read(0,b,256))>0){int i=0;while(i<n){if(b[i]>96&&b[i]<123)b[i]=b[i]-32;i++;}if(write(1,b,n)!=n)return 8;}',
        'return n<0;',
        '}',
    ]
    source_bytes = ("\n".join(source) + "\n").encode()
    binary = b"a\x00\x04z\n" + secrets.token_bytes(70)
    # Only lowercase ASCII bytes change; NUL and Ctrl-D are ordinary file bytes.
    transformed = bytes(c - 32 if 97 <= c <= 122 else c for c in binary)
    guest = Guest(work)
    generations = []
    with tempfile.TemporaryDirectory() as temp:
        socket = Path(temp) / "qmp.sock"
        try:
            guest.boot(disk=True, observer_socket=socket)
            read_prompt(guest)
            for name, data in inputs.items():
                receive(guest, name.encode(), data)
            receive(guest, b"input", binary)
            bootstrap(guest)
            for index in range(3):
                command(guest, b"build extra2", b"built\n")
                code = executable(guest, socket, 0x41100004, 65532)
                (work / f"compiler-{index}.bin").write_bytes(code)
                command(guest, b"install", b"installed\n")
                assert read_memory(socket, 0x40150000, len(code), work / "installed.bin") == code
                generations.append(code)
            assert generations[1] == generations[2]
            command(guest, b"build extra4", b"built\n")
            dev = executable(guest, socket, 0x41100004, 65532)
            (work / "development.bin").write_bytes(dev)
            guest.serial_send(b"exec dev\n".hex())
            until(guest, b"dev> ")
            enter(guest, b"exec absent", contains=b"status 2\n")

            def edit(lines):
                enter(guest, b"edit nova.c", b"edit> ")
                for line in lines:
                    enter(guest, line, b"edit> ")
                enter(guest, b"q", contains=b"status 0\n")

            edit([f"i {i} {line}".encode() for i, line in enumerate(source, 1)] + [b"w"])
            enter(guest, b"build nova.c", contains=b"built\nstatus 0\n")
            enter(guest, b"exec first", contains=marker.encode() + b"\nstatus 0\n")
            edit([b"r 4 return 1+;", b"w"])
            enter(guest, b"build nova.c", contains=b"status 1\n")
            enter(guest, b"exec retained", contains=marker.encode() + b"\nstatus 0\n")
            edit([b"r 4 " + source[3].encode(), b"i 5 puts(\"temporary\");", b"d 5", b"w"])
            edit([b"r 4 puts(\"discarded\");return 9;"])
            enter(guest, b"build nova.c", contains=b"status 0\n")
            enter(guest, b"exec after-edit", contains=marker.encode() + b"\nstatus 0\n")
            enter(guest, b"nova.c X < input | catbuild > output", contains=b"status 0\n")
            enter(guest, b"catbuild < output", contains=transformed + b"status 0\n")
            enter(guest, b"Check -n tail >> output", contains=b"status 0\n")
            enter(guest, b"catbuild output", contains=transformed + b"tailstatus 0\n")
            enter(guest, b"nova.c exit 2> errors | catbuild", contains=b"status 7\n")
            enter(guest, b"catbuild errors", contains=b"nested exit\nstatus 0\n")
            enter(guest, b"basebuild | catbuild", contains=b"status 1\n")
            enter(guest, b"catbuild < absent | catbuild", contains=b"status 1\n")
            enter(guest, b"Check bad > output | catbuild", contains=b"status 2\n")
            enter(guest, b"exec recovered", contains=marker.encode() + b"\nstatus 0\n")
            enter(guest, b"catbuild output | nova.c X | catbuild > errors", contains=b"status 0\n")
            enter(guest, b"catbuild errors", contains=transformed + b"TAILstatus 0\n")
            enter(guest, b"nova.c emit | nova.c X | catbuild > output", contains=b"status 0\n")
            enter(guest, b"catbuild output output | catbuild > errors", contains=b"No space left on device\nstatus 1\n")
            enter(guest, b"edit output", b"edit> ")
            enter(guest, b"i 1 overflow", b"edit> ", b"error: buffer capacity\n")
            enter(guest, b"q", contains=b"status 0\n")
            enter(guest, b"exec recovered-again", contains=marker.encode() + b"\nstatus 0\n")
            # Empty truncation must persist with no subsequent mutating operation.
            enter(guest, b"Check -n > output", contains=b"status 0\n")
            guest.stop()
            disk = (work / "disk.img").read_bytes()
            saved = {}
            for i in range(24):
                entry = disk[i * 128:(i + 1) * 128]
                if entry[0]:
                    name = entry[4:4 + entry[0]].decode()
                    size = int.from_bytes(entry[2:4], "little")
                    saved[name] = disk[4096 + i * 32768:4096 + i * 32768 + size]
            assert saved["nova.c"] == source_bytes
            assert saved["output"] == b""
            for name, data in inputs.items():
                assert saved[name] == data, name
            guest.boot(disk=True)
            read_prompt(guest)
            command(guest, b"cat output", b"\n")
            bootstrap(guest)
            command(guest, b"build extra2", b"built\n")
            command(guest, b"install", b"installed\n")
            command(guest, b"build extra4", b"built\n")
            guest.serial_send(b"exec dev\n".hex())
            until(guest, b"dev> ")
            enter(guest, b"catbuild nova.c", contains=source_bytes + b"status 0\n")
            enter(guest, b"build nova.c", contains=b"status 0\n")
            enter(guest, b"exec reboot", contains=marker.encode() + b"\nstatus 0\n")
            enter(guest, b"nova.c X < input | catbuild > output", contains=b"status 0\n")
            enter(guest, b"catbuild output", contains=transformed + b"status 0\n")
        finally:
            guest.stop()
    result = {"compiler_sizes": list(map(len, generations)), "compiler_sha256": hashlib.sha256(generations[2]).hexdigest(), "development_size": len(dev), "work": str(work)}
    (work / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
