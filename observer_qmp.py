"""Read guest RAM from the observer side of a verification run."""
import json
import socket


def read_memory(path, address, size, output):
    with socket.socket(socket.AF_UNIX) as connection:
        connection.settimeout(2)
        connection.connect(str(path))
        with connection.makefile("rb") as stream:
            json.loads(stream.readline())
            requests = [
                {"execute": "qmp_capabilities"},
                {"execute": "pmemsave", "arguments": {
                    "val": address, "size": size, "filename": str(output.resolve()),
                }},
            ]
            for request in requests:
                connection.sendall(json.dumps(request).encode() + b"\n")
                while line := stream.readline():
                    response = json.loads(line)
                    if "error" in response:
                        raise ValueError(response["error"]["desc"])
                    if "return" in response:
                        break
                else:
                    raise ValueError("QMP connection closed")
    return output.read_bytes()
