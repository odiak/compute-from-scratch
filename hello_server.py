"""The host-only HTTP origin used by the experiment."""

import json
import re
import secrets
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


PAGES = [
    ("HELLO WORLD", "TINY BROWSER"),
    ("BLUE MOON", "FRESH PAGE"),
    ("GREEN FIELD", "OPEN WINDOW"),
    ("RED FLOWER", "SMALL SCREEN"),
]


def html_page(heading, paragraph):
    return f"<html><body><h1>{heading}</h1><p>{paragraph}</p></body></html>".encode()


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pages = self.server.pages
        if pages and re.fullmatch(r"/[a-z0-9.\-]{0,23}", self.path):
            index = self.server.routes.setdefault(self.path, len(self.server.routes))
            body = pages[index % len(pages)]
        elif self.path == self.server.path:
            body = self.server.body
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", self.server.content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        with self.server.log.open("a") as stream:
            stream.write(json.dumps({"request": self.requestline, "body": body.decode()}) + "\n")

    def log_message(self, *_):
        pass


class HelloServer:
    def __init__(self, run, browser=False, paths=False):
        self.server = HTTPServer(("127.0.0.1", 0), HelloHandler)
        self.path = "/index.html" if browser else "/hello"
        self.paths = paths
        self.server.path = self.path
        self.server.routes = {}
        pages = secrets.SystemRandom().sample(PAGES, len(PAGES)) if paths else []
        self.server.pages = [html_page(*page) for page in pages]
        if browser:
            heading, paragraph = secrets.choice(PAGES)
            self.server.content_type = "text/html"
            self.server.body = html_page(heading, paragraph)
        else:
            self.server.content_type = "text/plain"
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
