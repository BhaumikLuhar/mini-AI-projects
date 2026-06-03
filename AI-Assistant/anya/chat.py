from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent.parent
SAVE_DIR = BASE_DIR / "chats"
SAVE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class ChatSession:

    def __init__(
        self,
        system_prompt: str,
        persona_name: str = "anya",
        max_context_tokens=8000
    ):
        self.system_prompt = (
            system_prompt
        )

        self.current_file = None

        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        self.max_context_tokens = max_context_tokens

        self.persona_name = persona_name

    def add_user(self, text: str):
        self.messages.append(
            {
                "role": "user",
                "content": text
            }
        )
        self.trim_history()
        self.save()

    def add_assistant(self, text: str):
        self.messages.append(
            {
                "role": "assistant",
                "content": text
            }
        )
        self.trim_history()
        self.save()

    def reset(self):
        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]
        self.current_file = None

    def save(self) -> str:
        if self.current_file is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            self.current_file = str(SAVE_DIR / f"chat-{timestamp}.json")

        filename = Path(self.current_file)

        with open(filename, "w", encoding="utf-8")as f:
            json.dump(self.messages, f, indent=2)

        return str(filename)

    def load(self, filename: str):
        path = Path(filename)

        if not path.is_absolute() and not path.exists():
            path = SAVE_DIR / path

        with open(path, "r", encoding="utf-8")as f:
            self.messages = json.load(f)

        self.system_prompt = self.messages[0]["content"]
        self.current_file = str(path)

    def get_messages(self):

        return self.messages

    def message_count(self):

        return len(
            self.messages
        )

    def estimate_message_tokens(self, message):
        return max(1, len(message["content"]) // 4)

    def total_tokens(self):
        return sum(self.estimate_message_tokens(message) for message in self.messages)

    def trim_history(self):

        while (self.total_tokens() > self.max_context_tokens):
            if len(self.messages) <= 3:
                break

            self.messages.pop(1)
