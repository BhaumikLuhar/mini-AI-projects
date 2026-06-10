from evals.common import (
    run_all_evaluations,
    write_report,
)
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main():
    report = run_all_evaluations()
    write_report(report)

    retrieval = report["retrieval"]
    answers = report["answers"]
    citations = report["citations"]
    hallucination = report["hallucination"]

    print(f"Recall@1: {retrieval['recall@1']:.2%}")
    print(f"Recall@3: {retrieval['recall@3']:.2%}")
    print(f"Recall@5: {retrieval['recall@5']:.2%}")
    print()
    print(f"Answer Accuracy: {answers['accuracy']:.2%}")
    print(f"Citation Accuracy: {citations['accuracy']:.2%}")
    print(f"Hallucination Resistance: {hallucination['success_rate']:.2%}")


if __name__ == "__main__":
    main()
