"""Build exact multi-line C source delivered through the guest's raw receiver."""
import secrets
import sys
import tempfile
from pathlib import Path

from guest_tool import Guest
from verify_c_subset import put_file
from verify_shell import command, read_prompt
from verify_source_import import receive


def main():
    root = Path(".local/c-lexing-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    scale = secrets.randbelow(12) + 2
    source = (
        "/* lead */ int\t g ( int /* parameter */ x ) {\r\n"
        f"\treturn x /* multiply */ * {scale};\n}}\v\f\n"
        "int f (int x) { // entry\n"
        "  int y = g /* call */ (x);\n"
        "  if (x) { y = y + 3; } // branch\n"
        "  return y;\n} // valid EOF"
    ).encode()
    try:
        guest.boot(disk=True)
        read_prompt(guest)
        put_file(guest, b"compiler", Path(sys.argv[2]).read_bytes().strip())
        command(guest, b"as compiler", b"assembled\n")
        command(guest, b"install", b"installed\n")
        receive(guest, b"code", source)
        command(guest, b"cat code", source + b"\n")
        command(guest, b"build code", b"built\n")
        for argument in (0, secrets.randbelow(20) + 3, secrets.randbelow(20) + 30):
            expected = argument * scale + (3 if argument else 0)
            command(guest, f"run {argument}".encode(), f"exit {expected:08x}\n".encode())
        for malformed in (
            b"int f(int x){return x;} /* never closed",
            b"in/**/t f(int x){return x;}",
            b"int f(int x){return 1/**/2;}",
        ):
            receive(guest, b"code", malformed)
            command(guest, b"build code", b"build error\n")
        command(guest, b"run 7", f"exit {7*scale+3:08x}\n".encode())
    finally:
        guest.stop()
    print(f"C lexical input verified: {workspace}")


if __name__ == "__main__":
    main()
