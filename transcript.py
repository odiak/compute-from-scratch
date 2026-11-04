"""Convert a campaign's Pi event logs into Markdown transcripts under experiments/.

Usage: python3 transcript.py CAMPAIGN_DIR [STAGE ...]

Without stages, every stage that already has experiments/NNN-campaign.md is converted.
"""
import base64
import html
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPERIMENTS = ROOT / "experiments"
FOLD = 1500
HOME = re.compile(r"/Users/[^/\s\"']+|/home/[^/\s\"']+")
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+")


CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def scrub(text):
    text = text.replace(str(ROOT), "$REPO")
    text = HOME.sub("~", text)
    text = JWT.sub("[REDACTED-JWT]", text)
    return CONTROL.sub(lambda m: "␡" if m.group() == "\x7f" else chr(0x2400 + ord(m.group())), text)


def prose(text):
    return html.escape(scrub(text), quote=False)


def fence(text, lang=""):
    run = max((len(m) for m in re.findall(r"`+", text)), default=0)
    ticks = "`" * max(3, run + 1)
    return f"{ticks}{lang}\n{text.rstrip()}\n{ticks}"


def block(text, label, lang=""):
    text = scrub(text)
    body = fence(text, lang)
    if len(text) <= FOLD:
        return body
    lines = text.count("\n") + 1
    return f"<details><summary>{label} ({len(text):,} chars, {lines:,} lines)</summary>\n\n{body}\n\n</details>"


def clock(start, ms):
    seconds = int((ms - start) / 1000)
    return f"+{seconds // 3600}:{seconds // 60 % 60:02}:{seconds % 60:02}"


def iso_ms(stamp):
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp() * 1000


def render_args(name, args):
    small = {k: v for k, v in args.items() if not (isinstance(v, str) and (len(v) > 80 or "\n" in v))}
    large = {k: v for k, v in args.items() if k not in small}
    head = f"**→ `{name}`**"
    if small:
        head += " " + "`" + scrub(json.dumps(small, ensure_ascii=False)) + "`"
    parts = [head]
    for key, value in large.items():
        parts.append(block(value, f"{key}"))
    return "\n\n".join(parts)


def render_result(name, content, stage, images):
    parts = []
    for item in content:
        if item.get("type") == "image":
            images.append(item)
            path = f"{stage}-transcript-{len(images):03}.png"
            (EXPERIMENTS / path).write_bytes(base64.b64decode(item["data"]))
            parts.append(f"![{name} image {len(images)}]({path})")
            continue
        text = item.get("text", "")
        try:
            value = json.loads(text)
        except ValueError:
            value = None
        if isinstance(value, dict) and any(isinstance(v, str) and "\n" in v for v in value.values()):
            for key, inner in value.items():
                inner = inner if isinstance(inner, str) else json.dumps(inner)
                parts.append(f"`{key}`\n\n" + block(inner, key))
        else:
            parts.append(block(text, "result"))
    return "\n\n".join(parts) if parts else "_(empty)_"


def convert(campaign, stage):
    events = [json.loads(line) for line in (campaign / f"{stage}-events.jsonl").open()]
    config = json.loads((campaign / f"{stage}-config.json").read_text())
    times = [iso_ms(e["timestamp"]) for e in events if isinstance(e.get("timestamp"), str)]
    times += [e["message"]["timestamp"] for e in events if isinstance(e.get("message", {}).get("timestamp"), int)]
    start, end = min(times), max(times)
    out, images = [], []
    totals = {"input": 0, "output": 0, "cacheRead": 0}
    calls = boots = compactions = continues = 0
    prompts = 0
    for event in events:
        kind = event["type"]
        if kind == "compaction_start":
            compactions += 1
            out.append(f"---\n\n## Compaction {compactions} ({event.get('reason')}) {clock(start, iso_ms(event['timestamp']))}")
        elif kind == "compaction_end":
            summary = (event.get("result") or {}).get("summary", "")
            out.append(block(summary, "Summary carried over") if summary else "_(no summary)_")
            out.append("---")
        if kind != "message_end":
            continue
        message = event["message"]
        role = message["role"]
        moment = message.get("timestamp") if isinstance(message.get("timestamp"), int) else None
        if moment is None and isinstance(event.get("timestamp"), str):
            moment = iso_ms(event["timestamp"])
        stamp = clock(start, moment) if moment is not None else ""
        content = message["content"]
        if role == "system":
            added = [t["name"] for t in message.get("toolsAdded", [])]
            if added:
                out.append(f"_Tools added: {', '.join(f'`{n}`' for n in added)}_")
        elif role == "user":
            prompts += 1
            if prompts > 1:
                continues += 1
            text = "".join(b.get("text", "") for b in content) if isinstance(content, list) else content
            title = "Stage prompt" if prompts == 1 else f"Observer message {prompts - 1}"
            out.append(f"## {title} {stamp}\n\n" + "\n".join("> " + line for line in prose(text).splitlines()))
        elif role == "assistant":
            for key in totals:
                totals[key] += message.get("usage", {}).get(key, 0)
            parts = [f"#### {stamp}"]
            for item in content:
                kind = item.get("type")
                if kind == "thinking" and item.get("thinking"):
                    parts.append("\n".join("> 💭 " + line for line in prose(item["thinking"]).splitlines() if line.strip()))
                elif kind == "text" and item.get("text"):
                    parts.append(prose(item["text"]))
                elif kind == "toolCall":
                    calls += 1
                    boots += item["name"].startswith("vm_boot")
                    parts.append(render_args(item["name"], item.get("arguments") or {}))
            out.append("\n\n".join(parts))
        elif role == "toolResult":
            mark = " ⚠️ error" if message.get("isError") else ""
            out.append(f"**← `{message.get('toolName')}`**{mark}\n\n" + render_result(message.get("toolName"), content, stage, images))
    header = [
        f"# {stage} — transcript",
        f"Mechanically converted from the Pi event log by [transcript.py](../transcript.py). Summary: [{stage}-campaign.md]({stage}-campaign.md). Control bytes appear as Unicode control pictures (␀, ␛, …), and `$REPO` stands for the repository root.",
        "| | |\n| --- | --- |\n"
        + f"| Model | `{config.get('provider')}/{config.get('model')}` |\n"
        + f"| Start (UTC) | {datetime.fromtimestamp(start / 1000, UTC):%Y-%m-%d %H:%M:%S} |\n"
        + f"| Duration | {clock(start, end)[1:]} |\n"
        + f"| Tool calls | {calls} |\n"
        + f"| VM boots | {boots} |\n"
        + f"| Observer messages | {continues} |\n"
        + f"| Compactions | {compactions} |\n"
        + f"| Tokens (input / cached / output) | {totals['input']:,} / {totals['cacheRead']:,} / {totals['output']:,} |",
        "**Tools:** " + ", ".join(f"`{t}`" for t in config.get("activeTools", [])),
        "**System prompt:**\n\n" + fence(scrub(config.get("systemPrompt", ""))),
    ]
    text = "\n\n".join(header + out) + "\n"
    leftover = HOME.search(text) or JWT.search(text)
    if leftover:
        raise ValueError(f"{stage}: unscrubbed text remains: {leftover.group()[:40]}")
    (EXPERIMENTS / f"{stage}-transcript.md").write_text(text)
    return len(text), len(images)


def main():
    campaign = Path(sys.argv[1])
    stages = sys.argv[2:] or sorted(
        p.name[:3] for p in EXPERIMENTS.glob("[0-9][0-9][0-9]-campaign.md") if (campaign / f"{p.name[:3]}-events.jsonl").exists()
    )
    for stage in stages:
        size, images = convert(campaign, stage)
        print(f"{stage}: {size:,} chars, {images} images")


if __name__ == "__main__":
    main()
