from openai import OpenAI
from dotenv import load_dotenv
import httpx

import os

load_dotenv()


LLM_MODEL = os.getenv(
    "MODEL2",
    "openai/gpt-4.1"
)

load_dotenv()

def get_client() -> OpenAI:
    api_key=os.getenv("GITHUB_API_KEY")
    if not api_key:
        raise ValueError(
            "GITHUB_API_KEY not found."
        )
    
    return OpenAI(
        api_key=api_key,
        base_url="https://models.github.ai/inference",
        http_client=httpx.Client(verify=False)
    )
