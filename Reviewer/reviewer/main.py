import argparse
from pathlib import Path

from reviewer.logger import logger
from reviewer.pipeline import prepare_document
from reviewer.report import (
    write_json_report,
    write_markdown_report,
)
from reviewer.state import (
    cost_tracker
)

def ensure_results_dir() -> None:
    """
    Create results directory if it does not exist.
    """
    Path("results").mkdir(exist_ok=True)


def process_document(file_path: str) -> bool:
    """
    Process a single document.

    Returns:
        bool: True if successful, False otherwise.
    """

    try:
        logger.info(
            f"Processing document: {file_path}"
        )

        result = prepare_document(file_path)

        report = result["report"]

        stem = Path(file_path).stem

        json_path = (
            Path("results")
            / f"{stem}.json"
        )

        md_path = (
            Path("results")
            / f"{stem}.md"
        )

        write_json_report(
            report,
            str(json_path),
        )

        write_markdown_report(
            report,
            str(md_path),
        )

        logger.info(
            f"Generated: {json_path}"
        )

        logger.info(
            f"Generated: {md_path}"
        )

        return True

    except Exception as e:

        logger.exception(
            f"Failed processing {file_path}"
        )

        return False


def process_batch(folder_path: str) -> None:
    """
    Process all PDF/TXT files
    in a directory.
    """

    folder = Path(folder_path)

    if not folder.exists():

        raise FileNotFoundError(
            f"Folder not found: {folder}"
        )

    files = []

    files.extend(
        folder.glob("*.pdf")
    )

    files.extend(
        folder.glob("*.txt")
    )

    if not files:

        logger.warning(
            "No PDF or TXT files found."
        )

        return

    success = 0
    failed = 0

    logger.info(
        f"Found {len(files)} document(s)"
    )

    for file_path in files:

        result = process_document(
            str(file_path)
        )

        if result:
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)

    print(f"Documents: {len(files)}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")

    print("=" * 60)
    cost_tracker.print_summary()


def main():

    parser = argparse.ArgumentParser(
        description=(
            "AI Document Review System"
        )
    )

    parser.add_argument(
        "path",
        help=(
            "PDF/TXT file path "
            "or folder path in batch mode"
        ),
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help=(
            "Process all PDF/TXT files "
            "inside a folder"
        ),
    )

    args = parser.parse_args()

    ensure_results_dir()

    if args.batch:

        process_batch(
            args.path
        )

    else:

        success = process_document(
            args.path
        )

        if success:

            print(
                "\nReview completed successfully."
            )

            cost_tracker.print_summary()

        else:

            print(
                "\nReview failed."
            )


if __name__ == "__main__":
    main()