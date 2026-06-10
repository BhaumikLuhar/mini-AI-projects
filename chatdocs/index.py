import sys

from chatdocs.indexer import (
    Indexer
)


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python index.py docs/"
        )

        return
    
    docs_dir = sys.argv[1]

    indexer=Indexer()

    summary=(
        indexer.index_folder(docs_dir)
    )

    print()

    print(
        f"Indexed: "
        f"{summary['indexed']}"
    )

    print(
        f"Skipped: "
        f"{summary['skipped']}"
    )

    print(
        f"Total: "
        f"{summary['total']}"
    )

if __name__ == "__main__":
    main()