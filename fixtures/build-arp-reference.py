"""Compile the observer fixture and extract its relocation-free ELF text."""
import struct
import subprocess
import tempfile
from pathlib import Path

source = Path(__file__).with_name("arp-reference.c")
with tempfile.TemporaryDirectory() as temp:
    obj = Path(temp) / "reference.o"
    subprocess.run(["clang", "--target=aarch64-none-elf", "-O2", "-ffreestanding",
                    "-fno-stack-protector", "-fno-vectorize", "-fno-slp-vectorize",
                    "-c", str(source), "-o", str(obj)], check=True)
    data = obj.read_bytes()
offset = struct.unpack_from("<Q", data, 40)[0]
size, count, index = struct.unpack_from("<HHH", data, 58)
sections = [struct.unpack_from("<IIQQQQIIQQ", data, offset + i * size) for i in range(count)]
_, _, _, _, start, length, *_ = sections[index]
names = data[start:start + length]
for name, kind, _, _, start, length, *_ in sections:
    if kind in (4, 9):
        raise SystemExit("Reference fixture unexpectedly contains relocations")
    if names[name:].split(b"\0", 1)[0] == b".text":
        text = data[start:start + length]
print(text.hex())
