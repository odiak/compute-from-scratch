"""The host-only HTTP origin used by the experiment."""
import json
import secrets
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/hello":
            self.send_error(404)
            return
        body = self.server.body
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        with self.server.log.open("a") as stream:
            stream.write(json.dumps({"request": self.requestline, "body": body.decode()}) + "\n")

    def log_message(self, *_):
        pass


class HelloServer:
    def __init__(self, run):
        self.server = HTTPServer(("127.0.0.1", 0), HelloHandler)
        self.server.body = b"Hello, world! " + secrets.token_hex(6).encode() + b"\n"
        self.server.log = run / "http.jsonl"
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def request(self, data):
        with socket.create_connection(self.server.server_address, timeout=2) as client:
            client.sendall(data)
            client.shutdown(socket.SHUT_WR)
            with client.makefile("rb") as stream:
                return stream.read(4096)

    def close(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
