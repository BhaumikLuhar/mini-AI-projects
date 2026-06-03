from anya.persona import PersonaManager
from anya.client import LLMClient
from anya.evaluator import Evaluator

def main():
    print("\n=== Running Anya Evaluation Suite ===\n")

    persona_manager = PersonaManager()

    system_prompt = (
        persona_manager.load_persona(
            "anya"
        )
    )

    client=LLMClient()

    evaluator=Evaluator("tests/eval_questions.json")

    results = evaluator.run_all(
        client,
        system_prompt
    )

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    total = len(results)

    accuracy = (
        passed / total * 100
        if total > 0
        else 0
    )

    print("=" * 60)

    for result in results:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"[{status}] "
            f"{result['question']}"
        )

        if not result["passed"]:

            print(
                f"Response: "
                f"{result['response']}"
            )

            print("-" * 60)

    print("\n=== Summary ===")

    print(
        f"Passed: "
        f"{passed}/{total}"
    )

    print(
        f"Accuracy: "
        f"{accuracy:.2f}%"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()