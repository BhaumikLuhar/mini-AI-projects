from openai import OpenAI

from chatdocs.config import Config

class LLMClient:

    def __init__(self):
        self.client=OpenAI(
            api_key=Config.GITHUB_TOKEN,
            base_url="https://models.github.ai/inference"
        )


    def generate(self, messages, temperature=0):

        response=self.client.chat.completions.create(
            model=Config.MODEL,
            messages=messages,
            temperature=temperature
        )

        return response.choices[0].message.content