"""Persistent VM broker. Closing stdin stops the VM."""
import json
import os
import subprocess
import sys
from pathlib import Path
from time import monotonic, sleep

from arp_link import ArpLink
from runner import prepare_run


class Guest:
    def __init__(self, workspace):
        self.workspace = workspace
        self.process = None
        self.link = None
        self.run = None
        self.offset = 0

    def boot(self, network=False):
        if self.process is not None:
            raise ValueError("Stop the current VM first")
        image = bytes.fromhex((self.workspace / "guest.hex").read_text())
        self.run, command, record = prepare_run(image, self.workspace / "runs")
        link = ArpLink() if network else None
        if link:
            fd = link.guest.fileno()
            command.extend([
                "-global", "virtio-mmio.force-legacy=false",
                "-netdev", f"socket,id=net0,fd={fd}",
                "-device", "virtio-net-device,netdev=net0,mac=52:54:00:12:34:56",
                "-object", "filter-dump,id=trace,netdev=net0,file=network.pcap",
            ])
            record["peer_mac"] = link.mac.hex(":")
        try:
            (self.run / "run.json").write_text(json.dumps(record, indent=2) + "\n")
            with (self.run / "serial.log").open("wb") as serial, (self.run / "qemu.log").open("wb") as log:
                self.process = subprocess.Popen(command, cwd=self.run, stdin=subprocess.PIPE,
                                                stdout=serial, stderr=log,
                                                pass_fds=(fd,) if link else ())
        except OSError:
            if link:
                link.close()
            raise
        if link:
            link.guest.close()
            link.thread.start()
        self.link = link
        self.offset = 0
        return {"run_id": self.run.name}

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process.stdin.close()
            self.process = None
        if self.link:
            self.link.close()
            self.link = None
        return {}

    def serial_read(self, wait_ms):
        if self.run is None:
            raise ValueError("Boot a VM first")
        if type(wait_ms) is not int or not 0 <= wait_ms <= 5000:
            raise ValueError("wait_ms must be an integer in 0..5000")
        deadline = monotonic() + wait_ms / 1000
        with (self.run / "serial.log").open("rb") as stream:
            stream.seek(self.offset)
            data = stream.read(4096)
            while not data and self.process is not None and self.process.poll() is None:
                remaining = deadline - monotonic()
                if remaining <= 0:
                    break
                sleep(min(remaining, 0.02))
                data = stream.read(4096)
            self.offset = stream.tell()
        return {"hex": data.hex(), "text": data.decode(errors="replace")}

    def serial_send(self, hex_text):
        data = bytes.fromhex(hex_text)
        if not 1 <= len(data) <= 256:
            raise ValueError("Send 1 to 256 bytes at a time")
        if self.process is None or self.process.poll() is not None:
            raise ValueError("Boot a VM first")
        os.set_blocking(self.process.stdin.fileno(), False)
        sent = os.write(self.process.stdin.fileno(), data)
        with (self.run / "serial-input.bin").open("ab") as stream:
            stream.write(data[:sent])
        return {"sent": sent}


def main():
    guest = Guest(Path(sys.argv[1]).resolve())
    operations = {
        "vm_boot": lambda _: guest.boot(),
        "vm_boot_network": lambda _: guest.boot(network=True),
        "vm_stop": lambda _: guest.stop(),
        "serial_read": lambda args: guest.serial_read(args.get("wait_ms", 0)),
        "serial_send": lambda args: guest.serial_send(args["hex"]),
    }
    try:
        for line in sys.stdin:
            request = json.loads(line)
            try:
                response = {"result": operations[request["name"]](request["args"])}
            except (OSError, ValueError, KeyError) as error:
                response = {"error": str(error)}
            print(json.dumps(response), flush=True)
    finally:
        guest.stop()


if __name__ == "__main__":
    main()
