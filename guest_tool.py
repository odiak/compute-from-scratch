"""Stdio MCP server exposing a single bounded guest execution tool."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / ".local" / "runs"
TOOL = {
    "name": "run_guest",
    "description": "Boot your raw AArch64 hex image for one second and read its serial output.",
    "inputSchema": {
        "type": "object",
        "properties": {"hex": {"type": "string", "maxLength": 65536}},
        "required": ["hex"],
        "additionalProperties": False,
    },
}


def run_guest(hex_text):
    if not isinstance(hex_text, str) or len(hex_text) > 65536:
        raise ValueError("hex must be a string of at most 65536 characters")
    image = bytes.fromhex(hex_text)
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "guest.hex"
        source.write_text(image.hex())
        result = subprocess.run(
            [sys.executable, str(ROOT / "runner.py"), str(source),
             "--runs", str(RUNS), "--seconds", "1"],
            capture_output=True, text=True, timeout=10,
        )
    if not result.stdout.strip():
        raise ValueError(result.stderr.strip())
    run = Path(result.stdout.strip())
    with (run / "serial.log").open("rb") as serial:
        data = serial.read(4097)
    return json.dumps({
        "run_id": run.name, "serial": data[:4096].decode("utf-8", errors="replace"),
        "truncated": len(data) > 4096, "exit_code": result.returncode,
    })


def handle(request):
    method = request["method"]
    if method == "initialize":
        return {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "guest", "version": "1"}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [TOOL]}
    if method == "tools/call" and request["params"]["name"] == TOOL["name"]:
        try:
            output = run_guest(request["params"]["arguments"]["hex"])
            return {"content": [{"type": "text", "text": output}]}
        except (ValueError, subprocess.TimeoutExpired) as error:
            return {"isError": True, "content": [{"type": "text", "text": str(error)}]}
    raise KeyError(method)


for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request:
        continue
    response = {"jsonrpc": "2.0", "id": request["id"]}
    try:
        response["result"] = handle(request)
    except KeyError:
        response["error"] = {"code": -32602, "message": "Unsupported request or parameters"}
    print(json.dumps(response), flush=True)
