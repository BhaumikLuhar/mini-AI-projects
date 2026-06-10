import json

from chatdocs.rag import (
    RAGEngine
)

with open(
    "evals/eval_questions.json"
) as f:

    tests = json.load(f)


rag=RAGEngine()

passed=0
failed=0

for test in tests:

    result=rag.answer(test["question"])

    answer=result["answer"].lower()

    success=True

    for keyword in test["expected_contains"]:
        if keyword.lower() not in answer:
            success=False

    sources=[source for source in result["citations"]]

    if test["expected_source"] not in sources:
        success=False

    if success:
        passed+=1
        print(
            f"PASS: "
            f"{test['question']}"
        )
    else:
        failed+=1
        print(
            f"FAIL: "
            f"{test['question']}"
        )
            
print()

print(
    f"Passed: {passed}"
)

print(
    f"Failed: {failed}"
)


hallucination_tests = [
    "What is the CEO salary?",
    "Where is the Mars office?"
]
passed=False
for question in hallucination_tests:
    result = rag.answer(
            question
        )
    
    if (
            "i don't see that"
            in result["answer"].lower()
        ):
        print(
            f"PASS: "
            f"{question}"
        )

    else:
        print(
            f"FAIL: "
            f"{question}"
        )