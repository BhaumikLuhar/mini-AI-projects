import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMClient:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY missing."
            )

        self.model = os.getenv("MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")

        self.client = OpenAI(api_key=api_key, base_url=(
            "https://api.groq.com/openai/v1"))

    def get_reply(self, messages):
        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3
            )
        )

        return {
            "text": response.choices[0].message.content,
            "usage": response.usage
        }

    def stream_reply(self, messages):

        stream = (
            self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                stream=True
            )
        )

        full_text = []

        for chunk in stream:

            delta = (
                chunk.choices[0]
                .delta
                .content
            )

            if delta:

                print(
                    delta,
                    end="",
                    flush=True
                )

                full_text.append(
                    delta
                )

        print()

        return "".join(
            full_text
        )

    def assess_confidence(self, question: str, answer: str):

        prompt = f"""
You are evaluating an AI response.

Question:
{question}

Answer:
{answer}

Rate confidence from 1 to 5.

Rules:
1 = very uncertain
2 = somewhat uncertain
3 = acceptable
4 = confident
5 = very confident

Return ONLY the number.
"""

        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )
        )

        text = (
            response.choices[0]
            .message.content
        )

        if text != None:
            text = text.strip()
            try:
                return int(text)
            except ValueError:
                return 3


def estimate_tokens(text):
    return max(
        1,
        len(text) // 4
    )
