#!/usr/bin/env python3
"""Run a raw AArch64 guest and record its serial output."""
import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ENTRY = 0x40200000
RAM_MIB = 64


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="raw image encoded as hexadecimal bytes")
    parser.add_argument("--runs", type=Path, default=Path(".local/runs"))
    parser.add_argument("--seconds", type=int, default=2, choices=range(1, 31),
                        metavar="1..30")
    args = parser.parse_args()
    try:
        image = bytes.fromhex(args.image.read_text())
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if not 4 <= len(image) <= RAM_MIB * 1024**2 - 0x200000:
        parser.error("image must fit in guest RAM and contain at least one instruction")

    qemu = shutil.which("qemu-system-aarch64")
    if qemu is None:
        parser.error("qemu-system-aarch64 is required")
    version = subprocess.check_output([qemu, "--version"], text=True).splitlines()[0]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run = args.runs.resolve() / run_id
    run.mkdir(parents=True)
    binary = run / "guest.bin"
    binary.write_bytes(image)
    command = [
        qemu, "-machine", "virt", "-cpu", "cortex-a53", "-accel", "tcg",
        "-smp", "1", "-m", str(RAM_MIB), "-nodefaults", "-display", "none",
        "-monitor", "none", "-serial", "stdio", "-nic", "none", "-no-reboot",
        "-device", f"loader,file=guest.bin,addr={ENTRY:#x},force-raw=on,cpu-num=0",
    ]
    record = {
        "id": run_id, "qemu": version, "command": command,
        "image_sha256": hashlib.sha256(image).hexdigest(), "seconds": args.seconds,
    }
    try:
        with (run / "serial.log").open("wb") as serial, (run / "qemu.log").open("wb") as log:
            result = subprocess.run(command, cwd=run, stdin=subprocess.DEVNULL,
                                    stdout=serial, stderr=log, timeout=args.seconds)
        record.update(status="exited", returncode=result.returncode)
    except subprocess.TimeoutExpired:
        record["status"] = "timeout"
    finally:
        (run / "run.json").write_text(json.dumps(record, indent=2) + "\n")
    print(run)
    return record.get("returncode", 0)


if __name__ == "__main__":
    raise SystemExit(main())
