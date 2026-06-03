from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class ConversationLogger:
    def __init__(self):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

        self.log_file=( LOG_DIR / f"{timestamp}.jsonl")

    def _write_event(self,event:dict):
        event["timestamp"]=(datetime.now().isoformat())

        with open(self.log_file,"a",encoding="utf-8")as f:
            f.write(json.dumps(event,ensure_ascii=False))
            f.write("\n")

    def log_user(self,message:str):
        self._write_event({
            "event": "user",
            "content": message
        })

    def log_assistant(self,message:str, input_tokens: int=0, output_tokens: int=0):
        self._write_event({
            "event": "assistant",
            "content": message,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        })

    def log_escalation(self, reason:str, user_message: str):
        self._write_event(
            {
                "event": "escalation",
                "reason": reason,
                "message": user_message
            }
        )