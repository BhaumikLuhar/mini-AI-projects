import json
import os
from typing import Any

from openai import OpenAI
from agent.config import get_openai_key
from dotenv import load_dotenv

from agent.executor import execute_tool
from agent.tool_definitions import TOOLS
from agent.safety import SafetyManager

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GITHUB_API_KEY"),
    base_url="https://models.inference.ai.azure.com"
)

SYSTEM_PROMPT = """
You are a Sales Operations Assistant.

You help sales representatives:

- Look up CRM history
- Check inventory
- Calculate quotes
- Draft emails

When users ask about products without
providing SKUs:

1. Use find_product.
2. Use list_inventory if needed.
3. Then check inventory.
4. Then calculate quotes.

When drafting emails:

1. Use CRM lookup first.
2. Use the customer's email address from CRM.
3. Pass recipient_email to draft_email.
4. Never invent email addresses.

Always use tools when needed.

Never claim to have performed actions
that were not actually performed.

Never send emails.
Only draft them.
"""


def estimate_cost_inr(usage):
    if not usage:
        return 0
    
    input_tokens=usage.prompt_tokens
    output_tokens=usage.completion_tokens

    usd_cost=(input_tokens / 1_000_000) * 0.40+ (output_tokens / 1_000_000) * 1.60

    inr_cost=usd_cost*95

    return round(inr_cost,4)


class SalesOpsAgent:

    def __init__(self):
        self.safety=SafetyManager()
        self.tool_history=[]

    def run(self,conversation_messages:list[dict[str, Any]]):
        self.tool_history=[]
        request_cost=0

        messages: list=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
        ]
        messages.extend(conversation_messages)

        while(self.safety.check_iteration_limit()):
            self.safety.increment_iteration()

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            cost = estimate_cost_inr(response.usage)
            request_cost+=cost
            self.safety.add_cost(cost)

            if not self.safety.check_cost_limit():
                return {
                    "response": "Session cost limit exceeded.",

                    "status": "cost_limit_exceeded",
                    "iterations": self.safety.iterations,
                    "cost": self.safety.session_cost
                }
            
            assistant_message=response.choices[0].message

            if not assistant_message.tool_calls:
                self.safety.iterations=0
                return {
                    "response": assistant_message.content,
                    "status": "completed",
                    "iterations": self.safety.iterations,
                    "cost": self.safety.session_cost,
                    "tool_history": self.tool_history
                }

            if assistant_message.tool_calls:
                messages.append(assistant_message)

                for tool_call in assistant_message.tool_calls:
                    if tool_call.type != "function":
                        continue
                    tool_name=tool_call.function.name
                    tool_args=json.loads(tool_call.function.arguments)

                    tool_result=execute_tool(tool_name, tool_args)

                    self.tool_history.append({
                        "tool":tool_name,
                        "input":tool_args,
                        "output":tool_result
                    })

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id":
                                tool_call.id,
                            "content":
                                json.dumps(tool_result)
                        }
                    )

            
        return {
                "response": "Iteration limit reached.",
                "status": "iteration_limit",
                "iterations": self.safety.iterations,
                "request_cost":request_cost,
                "session_cost": self.safety.session_cost
            }