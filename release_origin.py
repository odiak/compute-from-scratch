"""Serve a single pinned upstream source over the isolated experiment link."""
import hashlib
import io
import json
import tarfile
from urllib.request import HTTPRedirectHandler, build_opener


ARCHIVE_URL = "https://dl.suckless.org/sbase/sbase-0.1.tar.gz"
ARCHIVE_SHA256 = "86f6bb67bcc7df3ba7a3f11da72eaeb2cf58c23e9a35a7dbcd316395d934c634"
SOURCE_SHA256 = "117c10e0e5a5139a80490673a3f14dd1dfcc45856adb84a83b28e3b301f1b48c"
SOURCE_MEMBER = "sbase-0.1/echo.c"
SOURCE_PATH = "/echo.c"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def upstream_source():
    with build_opener(NoRedirect()).open(ARCHIVE_URL, timeout=10) as response:
        archive = response.read(256 * 1024 + 1)
    if hashlib.sha256(archive).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Upstream archive hash did not match")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        member = tar.getmember(SOURCE_MEMBER)
        if not member.isfile() or member.size != 421:
            raise ValueError("Upstream source member did not match")
        with tar.extractfile(member) as stream:
            source = stream.read()
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise ValueError("Upstream source hash did not match")
    return source


class ReleaseOrigin:
    path = "/hello"
    paths = True

    def __init__(self, run):
        self.log = run / "release.jsonl"

    def request(self, data):
        line = data.split(b"\r\n", 1)[0]
        record = {"request": line.decode("ascii", errors="replace")}
        if line == b"GET /hello HTTP/1.0":
            status, body = b"200 OK", b"Release origin ready\n"
        elif line == f"GET {SOURCE_PATH} HTTP/1.0".encode():
            record["upstream"] = ARCHIVE_URL
            try:
                body = upstream_source()
                status = b"200 OK"
                record.update(archive_sha256=ARCHIVE_SHA256, source_sha256=SOURCE_SHA256)
            except (OSError, ValueError, tarfile.TarError, KeyError) as exc:
                status, body = b"502 Bad Gateway", b"Upstream source unavailable\n"
                record["error"] = str(exc)
        else:
            status, body = b"404 Not Found", b"Path not allowed\n"
        record.update(status=int(status[:3]), bytes=len(body))
        with self.log.open("a") as stream:
            stream.write(json.dumps(record) + "\n")
        return (b"HTTP/1.0 " + status + b"\r\nContent-Type: text/plain\r\nContent-Length: " +
                str(len(body)).encode() + b"\r\n\r\n" + body)

    def close(self):
        pass
