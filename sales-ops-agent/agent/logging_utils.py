import json
from datetime import datetime
from pathlib import Path

log_dir=Path("logs")

log_dir.mkdir(exist_ok=True)

def get_log_file():
    today=datetime.now().strftime("%Y-%m-%d")

    return log_dir / f"agent-{today}.jsonl"


def log_tool_call(tool_name,tool_input,tool_output,latency_ms):

    entry = {
        "timestamp":
            datetime.now()
            .isoformat(),

        "tool":
            tool_name,

        "input":
            tool_input,

        "output":
            tool_output,

        "latency_ms":
            latency_ms
    }

    with open(get_log_file(),"a",encoding="utf-8")as f:
        f.write(json.dumps(entry,ensure_ascii=False)+"\n")