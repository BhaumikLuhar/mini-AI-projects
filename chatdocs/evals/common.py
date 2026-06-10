from chatdocs.hybrid_retriever import (
    HybridRetriever
)
from chatdocs.rag import (
    RAGEngine
)
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "qa_pairs.json"
REPORT_PATH = ROOT / "eval_report.json"


def load_dataset(path: Path | None = None):
    dataset_path = path or DATASET_PATH

    if not dataset_path.exists():
        return []

    with open(dataset_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_report(report, path: Path | None = None):
    report_path = path or REPORT_PATH

    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)


def answer_contains_keywords(answer, keywords):
    normalized = answer.lower()

    for keyword in keywords:
        if keyword.lower() not in normalized:
            return False

    return True


def citations_include_source(citations, expected_source):
    sources = [source for source, _ in citations]
    return expected_source in sources


def retrieval_hit(results, expected_source):
    for result in results:
        if result.get("source") == expected_source:
            return True

    return False


def run_retrieval_eval(dataset=None):
    tests = dataset if dataset is not None else load_dataset()
    retriever = HybridRetriever()

    recall_1 = 0
    recall_3 = 0
    recall_5 = 0

    for test in tests:
        results = retriever.search(test["question"], top_k=5)

        if retrieval_hit(results[:1], test["expected_source"]):
            recall_1 += 1

        if retrieval_hit(results[:3], test["expected_source"]):
            recall_3 += 1

        if retrieval_hit(results[:5], test["expected_source"]):
            recall_5 += 1

    total = len(tests) or 1

    return {
        "recall@1": recall_1 / total,
        "recall@3": recall_3 / total,
        "recall@5": recall_5 / total,
    }


def run_answer_eval(dataset=None):
    tests = dataset if dataset is not None else load_dataset()
    rag = RAGEngine()

    answer_hits = 0
    citation_hits = 0

    for test in tests:
        response = rag.answer(test["question"])

        if answer_contains_keywords(
            response.get("answer", ""),
            test.get("expected_keywords", [])
        ):
            answer_hits += 1

        if citations_include_source(
            response.get("citations", []),
            test["expected_source"]
        ):
            citation_hits += 1

    total = len(tests) or 1

    return {
        "accuracy": answer_hits / total,
        "citation_accuracy": citation_hits / total,
    }


def run_hallucination_eval(questions=None):
    if questions is None:
        test_questions = [
            "What is CEO salary?",
            "What is our Mars office address?",
            "What stock exchange are we listed on?",
        ]
    else:
        test_questions = questions

    rag = RAGEngine()
    success_hits = 0

    for question in test_questions:
        response = rag.answer(question)

        if "don't see that" in response.get("answer", "").lower():
            success_hits += 1

    total = len(test_questions) or 1

    return {
        "success_rate": success_hits / total,
    }


def run_all_evaluations():
    dataset = load_dataset()

    retrieval = run_retrieval_eval(dataset)
    answers = run_answer_eval(dataset)
    hallucination = run_hallucination_eval()

    return {
        "retrieval": retrieval,
        "answers": {
            "accuracy": answers["accuracy"],
        },
        "citations": {
            "accuracy": answers["citation_accuracy"],
        },
        "hallucination": hallucination,
    }
