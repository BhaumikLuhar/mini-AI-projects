MAX_HISTORY_MESSAGES = 20


def trim_conversation(messages):

    if len(messages) <= MAX_HISTORY_MESSAGES:
        return messages

    return messages[-MAX_HISTORY_MESSAGES:]