"""Fixed screen and keyboard operations on a display-enabled VM."""
import json
import socket
from time import sleep


class Display:
    def __init__(self):
        self.host, self.guest = socket.socketpair()
        self.host.settimeout(3)
        self.stream = self.host.makefile("rb")
        self.ready = False
        self.count = 0

    def command(self, name, arguments=None):
        if not self.ready:
            if not self.stream.readline():
                raise ValueError("Display connection closed")
            self.ready = True
            self.command("qmp_capabilities")
        request = {"execute": name}
        if arguments:
            request["arguments"] = arguments
        self.host.sendall(json.dumps(request).encode() + b"\n")
        while line := self.stream.readline():
            response = json.loads(line)
            if "error" in response:
                raise ValueError(response["error"]["desc"])
            if "return" in response:
                return response["return"]
        raise ValueError("Display connection closed")

    def capture(self, run, fmt="png"):
        self.count += 1
        filename = f"screen-{self.count:03}.{fmt}"
        self.command("screendump", {"filename": filename, "format": fmt})
        return run / filename

    def key(self, key):
        if key not in ("left", "right", "up", "down", "ret", "esc"):
            raise ValueError("Unsupported guest key")
        self.press(key)

    def press(self, key):
        self.command("input-send-event", {"events": [
            {"type": "key", "data": {"down": down, "key": {"type": "qcode", "data": key}}}
            for down in (True, False)
        ]})

    def type_path(self, path):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
        punctuation = {"/": "slash", ".": "dot", "-": "minus"}
        if not 1 <= len(path) <= 24 or any(c not in alphabet and c not in punctuation for c in path):
            raise ValueError("Use 1 to 24 lowercase letters, digits, slashes, dots, or hyphens")
        for char in path:
            self.press(punctuation.get(char, char))
            sleep(0.03)

    def close(self):
        self.stream.close()
        self.host.close()
        self.guest.close()
