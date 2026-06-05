from dataclasses import dataclass
from typing import Type
from typing import TypeVar, Type
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from reviewer.config import LLM_MODEL, get_client
from reviewer.utils import estimate_tokens
from reviewer.state import cost_tracker
from reviewer.cost_tracker import UsageRecord

T=TypeVar("T", bound=BaseModel)
@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int


client: OpenAI = get_client()


def clean_json_response(text: str) -> str:
    """
    Remove markdown code fences that models
    sometimes wrap around JSON responses.
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace(
            "```json",
            "",
            1
        )

    if text.startswith("```"):
        text = text.replace(
            "```",
            "",
            1
        )

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_json(prompt: str) -> LLMResult:
    """
    Send prompt to model and return response
    along with estimated token counts.
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    text = response.choices[0].message.content

    if text is None:
        raise RuntimeError(
            "Model returned empty content."
        )

    return LLMResult(
        text=text,
        input_tokens=estimate_tokens(prompt),
        output_tokens=estimate_tokens(text),
    )


def validate_with_retry(
    prompt: str,
    model_class: Type[T],
    retries: int = 2,
)->T:
    """
    Generate JSON, validate with Pydantic,
    and retry if validation fails.
    """

    current_prompt = prompt

    for attempt in range(retries + 1):

        llm_result = generate_json(
            current_prompt
        )

        raw = clean_json_response(
            llm_result.text
        )

        try:

            validated = (
                model_class
                .model_validate_json(raw)
            )

            cost_tracker.add_record(
                UsageRecord(
                    document_name="unknown",
                    input_tokens=(
                        llm_result.input_tokens
                    ),
                    output_tokens=(
                        llm_result.output_tokens
                    ),
                    total_tokens=(
                        llm_result.input_tokens
                        + llm_result.output_tokens
                    ),
                    estimated_cost_usd=(
                        (
                            llm_result.input_tokens
                            + llm_result.output_tokens
                        )
                        * 0.000001
                    ),
                )
            )

            return validated

        except ValidationError as e:

            if attempt == retries:
                raise

            current_prompt = f"""
Original task:

{prompt}

--------------------------------------------------

Your previous response was invalid.

Validation error:

{str(e)}

Previous response:

{raw}

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- No code fences.
- Match the schema exactly.

Reply with corrected JSON only.
"""


    raise RuntimeError(
        "Validation failed after all retries."
    )