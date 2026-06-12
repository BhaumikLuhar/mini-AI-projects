import json

from tests.scenarios import (
    SCENARIOS
)

from agent.loop import (
    SalesOpsAgent
)

results = []

for scenario in SCENARIOS:

    agent = SalesOpsAgent()

    response = agent.run(
        [
            {
                "role": "user",
                "content":
                    scenario["prompt"]
            }
        ]
    )

    tools_used = [

        tool["tool"]

        for tool in
        response.get(
            "tool_history",
            []
        )
    ]

    passed = all(
        tool in tools_used

        for tool in
        scenario["expected_tools"]
    )

    results.append(
        {
            "scenario":
                scenario["name"],

            "passed":
                passed,

            "tools_used":
                tools_used
        }
    )

with open(
    "tests/results.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=2
    )

print(results)