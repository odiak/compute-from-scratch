"""Rebuild stage041 twice from declared source-only inputs, then use saved tools."""
import hashlib
import json
import secrets
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from time import monotonic

from guest_tool import Guest
from observer_qmp import read_memory
from verify_development import enter, until
from verify_shell import read_prompt
from verify_source_import import receive


OUTPUTS = ("ccbin", "ccbin.2", "devbin", "devbin.2", "cat", "basename", "echo", "sha")


def archive(data):
    entries = {}
    at = 0
    while at < len(data) and data[at]:
        width = data[at]
        size = int.from_bytes(data[at + 1:at + 3], "little")
        name = data[at + 3:at + 3 + width].decode()
        start = at + 3 + width
        entries[name] = data[start:start + size]
        at = start + size
    assert at == len(data) - 1 and data[at] == 0
    return entries


def files(disk):
    result = {}
    for i in range(24):
        entry = disk[i * 128:(i + 1) * 128]
        if entry[0]:
            name = entry[4:4 + entry[0]].decode()
            size = int.from_bytes(entry[2:4], "little")
            result[name] = disk[4096 + i * 32768:4096 + i * 32768 + size]
    return result


def code(saved, name):
    data = saved[name]
    size = int.from_bytes(data[:4], "little")
    if size + 4 > 32768:
        data += saved[name + ".2"]
    assert 4 <= size <= 65532 and size % 4 == 0 and len(data) == size + 4
    return data[4:]


def batch(guest, name=b"bootplan"):
    guest.serial_send((b"batch " + name + b"\n").hex())
    return until(guest, b"plan complete\nexit 00000000\nshell> ", timeout=60)


def main():
    snapshot = Path(sys.argv[1])
    expected_outputs = None
    refs = dict(zip(("echo", "cat", "basename"), (Path(p).resolve() for p in sys.argv[2:5])))
    if snapshot.is_file():
        manifest = json.loads(snapshot.read_text())
        expected_outputs = manifest.get("outputs")
        repo = Path(__file__).resolve().parent
        kernel = repo / manifest["kernel"]["path"]
        assert hashlib.sha256(bytes.fromhex(kernel.read_text())).hexdigest() == manifest["kernel"]["sha256"]
        inputs = {}
        for name, description in manifest["inputs"].items():
            data = (repo / description["path"]).read_bytes()
            assert len(data) == description["size"]
            assert hashlib.sha256(data).hexdigest() == description["sha256"]
            inputs[name] = data
        members = {name: archive(inputs[name]) for name in ("sources", "controls")}
        for name, entries in members.items():
            descriptions = manifest["archives"][name]["members"]
            assert set(entries) == set(descriptions)
            for member, data in entries.items():
                description = descriptions[member]
                assert data == (repo / description["path"]).read_bytes()
                assert hashlib.sha256(data).hexdigest() == description["sha256"]
        names = members["controls"]["inputs"].decode().split()
        assert set(names) == set(inputs)
    else:
        kernel = snapshot / "guest.hex"
        saved = files((snapshot / "disk.img").read_bytes())
        members = {name: archive(saved[name]) for name in ("sources", "controls", "seedpack")}
        names = members["controls"]["inputs"].decode().split()
        inputs = {}
        for name in names:
            if name in saved:
                inputs[name] = saved[name]
            else:
                inputs[name] = next(group[name] for group in members.values() if name in group)
    assert not set(inputs).intersection(OUTPUTS)
    for name, upstream in (("alpha", "cat.c"), ("beta", "basename.c"),
                           ("extra5", "echo.c"), ("Abc123xyz789", "arg.h")):
        assert members["sources"][name] == Path("fixtures/sbase-0.1", upstream).read_bytes()
    root = Path(".local/environment-rebuild-check")
    root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=root)).resolve()
    reference_dir = work / "reference"
    reference_dir.mkdir()
    builds = []

    def workspace(name):
        path = work / name
        path.mkdir()
        shutil.copyfile(kernel, path / "guest.hex")
        return path

    for iteration in range(2):
        path = workspace(f"clean-{iteration}")
        guest = Guest(path)
        with tempfile.TemporaryDirectory() as temp:
            socket = Path(temp) / "qmp.sock"
            try:
                guest.boot(disk=True, observer_socket=socket)
                read_prompt(guest)
                for name, data in inputs.items():
                    receive(guest, name.encode(), data)
                output = batch(guest)
                (path / "rebuild-output.bin").write_bytes(output)
                assert output.count(b"compiler bytes identical\n") == 2
                if expected_outputs is not None:
                    image = bytes.fromhex(kernel.read_text())
                    assert f"{hashlib.sha256(image).hexdigest()}  memory {len(image)}\n".encode() in output
                for group in (inputs, members["sources"], members["controls"]):
                    for name, data in group.items():
                        line = f"{hashlib.sha256(data).hexdigest()}  {name} {len(data)}\n".encode()
                        assert line in output, (name, "input inventory differs")
                installed = read_memory(socket, 0x40150000, 65412, path / "installed.bin")
            finally:
                guest.stop()
        built = files((path / "disk.img").read_bytes())
        assert code(built, "ccbin") == installed
        builds.append({name: built[name] for name in OUTPUTS})
        for name in OUTPUTS:
            assert f"{hashlib.sha256(built[name]).hexdigest()}  {name} {len(built[name])}\n".encode() in output
            if expected_outputs is not None:
                assert expected_outputs[name] == {"size": len(built[name]),
                                                  "sha256": hashlib.sha256(built[name]).hexdigest()}
        assert built["sources"] == inputs["sources"]
        assert built["controls"] == inputs["controls"]
        assert archive(built["seedpack"]) == {name: inputs[name] for name in ("new1", "extra1", "extra3")}
        if iteration == 1:
            assert builds[0] == builds[1], "Clean rebuild outputs differ"

    # A failed bootstrap must stop before installing the previous build again.
    for label, changes, expected, installs in (
        ("bad-assembly", {"new1": b"not an instruction;"}, b"assembly error\n", 0),
        ("bad-c", {"extra1": b"int main(){return 1+;}"}, b"build error\n", 1),
        ("missing-source", {"raw": None}, b"not found\n", 3),
    ):
        path = workspace(label)
        guest = Guest(path)
        try:
            guest.boot(disk=True)
            read_prompt(guest)
            for name, original in inputs.items():
                data = changes.get(name, original)
                if data is not None:
                    receive(guest, name.encode(), data)
            guest.serial_send(b"batch bootplan\n".hex())
            output = bytearray()
            for _ in range(10):
                output.extend(bytes.fromhex(guest.serial_read(100)["hex"]))
                if len(output) > 65536:
                    raise ValueError(f"{label}: excessive output ({len(output)} bytes), "
                                     f"first={bytes(output[:100])!r}")
            (path / "failure-output.bin").write_bytes(output)
            assert expected in output, (label, repr(output[:300]))
            assert output.count(b"installed\n") == installs, (label, repr(output[:300]))
            assert b"plan complete" not in output and b"exec dev" not in output
            guest.serial_send(b"echo recovered\n".hex())
            until(guest, b"recovered\nshell> ", timeout=5)
        finally:
            guest.stop()

    # Load the generated environment after a real reboot, without compiling a loader.
    path = work / "clean-1"
    guest = Guest(path)
    marker = "Rebuilt-" + secrets.token_hex(4)
    source = [
        '#include "libc"',
        'int main(int ac,char **av){',
        'int n=0;char *b=(char *)(16624*256*256+1024*256);',
        'if(ac<2){puts("' + marker + '");return 0;}',
        'if(!strcmp(av[1],"exit")){out(2,"nested exit\\n");exit(7);}',
        'while((n=read(0,b,256))>0){int i=0;while(i<n){if(b[i]>96&&b[i]<123)b[i]=b[i]-32;i++;}if(write(1,b,n)!=n)return 8;}',
        'return n<0;',
        '}',
    ]
    source_bytes = ("\n".join(source) + "\n").encode()
    binary = b"a\x00\x04z\n" + secrets.token_bytes(70)
    transformed = bytes(c - 32 if 97 <= c <= 122 else c for c in binary)

    def load():
        guest.serial_send(b"enter devbin devbin.2 dev restore ccbin ccbin.2\n".hex())
        until(guest, b"dev> ")

    def check(line, expected, status=0):
        result = enter(guest, line.encode())
        target = expected + f"status {status}\ndev> ".encode()
        assert result == target, (line, repr(result[:300]), repr(target[:300]))

    def compare(program, args):
        result = subprocess.run([program, *args], executable=str(refs[program]),
                                cwd=reference_dir, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=False)
        check("@" + " ".join([program, *args]), result.stdout, result.returncode)

    def edit(commands):
        enter(guest, b"edit nova.c", b"edit> ")
        for line in commands:
            enter(guest, line, b"edit> ")
        enter(guest, b"q", contains=b"status 0\n")

    try:
        guest.boot(disk=True)
        read_prompt(guest)
        receive(guest, b"input", binary)
        (reference_dir / "input").write_bytes(binary)
        load()
        for name in ("utilh", "stdioh", "stringh", "fcntlh"):
            check("remove " + name, b"")
        for args in ([], ["one", "two"], ["-n", "tail"], ["-z"]):
            compare("echo", args)
        for args in (["/dir/thing.c", ".c"], ["/"], ["foo", "foo"], [], ["-z"], ["a", "b", "c"]):
            compare("basename", args)
        for args in (["input"], ["-u", "input"], ["absent", "input"], ["-z"]):
            compare("cat", args)
        check("@cat < input | @cat", binary)
        edit([f"i {i} {line}".encode() for i, line in enumerate(source, 1)] + [b"w"])
        enter(guest, b"build nova.c", contains=b"built\nstatus 0\n")
        check("exec fresh", marker.encode() + b"\n")
        edit([b"r 4 return 1+;", b"w"])
        enter(guest, b"build nova.c", contains=b"status 1\n")
        check("exec retained", marker.encode() + b"\n")
        edit([b"r 4 " + source[3].encode(), b"i 5 puts(\"temporary\");", b"d 5", b"w"])
        edit([b"r 4 puts(\"discarded\");return 9;"])
        enter(guest, b"build nova.c", contains=b"status 0\n")
        check("exec fixed", marker.encode() + b"\n")
        enter(guest, b"nova.c X < input | @cat | @cat > output", contains=b"status 0\n")
        check("@cat output", transformed)
        check("@echo -n tail >> output", b"")
        check("@cat output", transformed + b"tail")
        enter(guest, b"nova.c exit 2> errors | @cat", contains=b"status 7\n")
        check("@cat errors", b"nested exit\n")
        enter(guest, b"@cat < absent | @cat", contains=b"status 1\n")
        enter(guest, b"@echo bad > output | @cat", contains=b"status 2\n")
        check("exec recovered", marker.encode() + b"\n")
        check("@sha input", f"{hashlib.sha256(binary).hexdigest()}  input {len(binary)}\n".encode())
        check("@echo -n > output", b"")
        guest.stop()
        persisted = files((path / "disk.img").read_bytes())
        assert persisted["nova.c"] == source_bytes and persisted["output"] == b""
        for name in OUTPUTS:
            assert persisted[name] == builds[1][name]
        guest.boot(disk=True)
        read_prompt(guest)
        load()
        check("@cat nova.c", source_bytes)
        check("@cat output", b"")
        enter(guest, b"build nova.c", contains=b"status 0\n")
        check("exec reboot", marker.encode() + b"\n")
        enter(guest, b"nova.c X < input | @cat > output", contains=b"status 0\n")
        check("@cat output", transformed)
    finally:
        guest.stop()

    result = {"work": str(work), "inputs": names,
              "kernel_sha256": hashlib.sha256(bytes.fromhex(kernel.read_text())).hexdigest(),
              "compiler_size": len(code(builds[0], "ccbin")),
              "compiler_sha256": hashlib.sha256(code(builds[0], "ccbin")).hexdigest(),
              "outputs": {name: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                          for name, data in builds[0].items()}}
    (work / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
