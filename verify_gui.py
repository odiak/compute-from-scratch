"""Verify framebuffer content and navigation through actual guest keys."""
import sys
import tempfile
from pathlib import Path
from time import monotonic, sleep

from guest_tool import Guest
from verify_shell import command, read_prompt


def read_panel_state(guest):
    screenshot = guest.display.capture(guest.run, fmt="ppm")
    magic, dimensions, maximum, pixels = screenshot.read_bytes().split(b"\n", 3)
    if (magic, dimensions, maximum) != (b"P6", b"160 120", b"255"):
        return None

    def pixel(x, y):
        offset = (160 * y + x) * 3
        return tuple(pixels[offset:offset+3])

    if pixel(0, 0) != (16, 24, 32):
        return None
    left, right = pixel(43, 60), pixel(115, 60)
    if pixel(18, 38) != left or pixel(90, 38) != right:
        return None
    active, inactive = (64, 192, 240), (48, 64, 80)
    if (left, right) == (active, inactive):
        return "left"
    if (left, right) == (inactive, active):
        return "right"
    return None


def expect(guest, expected):
    deadline = monotonic() + 5
    while monotonic() < deadline:
        if read_panel_state(guest) == expected:
            guest.display.capture(guest.run)
            return
        sleep(0.05)
    raise ValueError(f"Screen did not show {expected} as active")


def main():
    root = Path(".local/gui-check")
    root.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(dir=root)).resolve()
    (workspace / "guest.hex").write_text(Path(sys.argv[1]).read_text())
    guest = Guest(workspace)
    try:
        guest.boot(disk=True, display=True)
        read_prompt(guest)
        expect(guest, "left")
        guest.key_send("right")
        expect(guest, "right")
        command(guest, b"echo GUI", b"GUI\n")
        guest.key_send("left")
        expect(guest, "left")
    finally:
        guest.stop()
    print(f"GUI verified: {workspace}")


if __name__ == "__main__":
    main()
