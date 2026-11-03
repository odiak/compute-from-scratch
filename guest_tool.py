"""Stdio MCP server exposing bounded guest execution tools."""
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

INPUT_TOOL = {
    "name": "run_guest_with_input",
    "description": "Boot a fresh guest, supply one serial input byte, and read its output.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hex": TOOL["inputSchema"]["properties"]["hex"],
            "byte": {"type": "integer", "minimum": 0, "maximum": 255},
        },
        "required": ["hex", "byte"],
        "additionalProperties": False,
    },
}
TOOLS = [TOOL, INPUT_TOOL]


def run_guest(hex_text, serial_byte=None):
    if not isinstance(hex_text, str) or len(hex_text) > 65536:
        raise ValueError("hex must be a string of at most 65536 characters")
    image = bytes.fromhex(hex_text)
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "guest.hex"
        source.write_text(image.hex())
        command = [sys.executable, str(ROOT / "runner.py"), str(source),
                   "--runs", str(RUNS), "--seconds", "1"]
        if serial_byte is not None:
            command.extend(["--serial-byte", str(serial_byte)])
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
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
        return {"tools": TOOLS}
    if method == "tools/call":
        name = request["params"]["name"]
        args = request["params"]["arguments"]
        try:
            if name == TOOL["name"]:
                output = run_guest(args["hex"])
            elif name == INPUT_TOOL["name"]:
                byte = args["byte"]
                if type(byte) is not int or not 0 <= byte <= 255:
                    raise ValueError("byte must be an integer in 0..255")
                output = run_guest(args["hex"], byte)
            else:
                raise KeyError(name)
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
