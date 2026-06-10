from evals.common import (
    run_answer_eval,
)
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main():
    report = run_answer_eval()

    print(f"Answer Accuracy: {report['accuracy']:.2%}")
    print(f"Citation Accuracy: {report['citation_accuracy']:.2%}")


if __name__ == "__main__":
    main()
