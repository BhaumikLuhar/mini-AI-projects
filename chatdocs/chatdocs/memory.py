class ConversationMemory:

    def __init__(
        self,
        max_messages=10
    ):
        self.max_messages = (
            max_messages
        )

        self.messages = []


    def add_user(
        self,
        text
    ):
        self.messages.append(
            {
                "role": "user",
                "content": text
            }
        )

        self.trim()


    def add_assistant(
        self,
        text
    ):
        self.messages.append(
            {
                "role": "assistant",
                "content": text
            }
        )

        self.trim()


    def get_messages(self):
        return self.messages


    def clear(self):
        self.messages.clear()


    def trim(self):
        self.messages = (
            self.messages[
                -self.max_messages:
            ]
        )