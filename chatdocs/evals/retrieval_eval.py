from evals.common import (
    run_retrieval_eval,
)
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main():
    report = run_retrieval_eval()

    print(f"Recall@1: {report['recall@1']:.2%}")
    print(f"Recall@3: {report['recall@3']:.2%}")
    print(f"Recall@5: {report['recall@5']:.2%}")


if __name__ == "__main__":
    main()
