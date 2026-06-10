from chatdocs.rag import (
    RAGEngine
)

def print_banner():

    print()

    print(
        "ChatDocs Assistant"
    )

    print(
        "Type /help for commands."
    )

    print()


def print_help():

    print()

    print("/sources")

    print("/clear")

    print("/help")

    print("/exit")

    print()


def handle_source(rag):

    sources=rag.list_sources()

    print()

    for source in sources:

        print(f"- {source}")

    print()



def main():

    rag=RAGEngine()

    print_banner()

    while True:

        if rag.retriever.indexer.count()==0:
            print()
            print("No indexed documents found.")
            print()
            print("Run : python index.py docs/")

        question=input("You : ").strip()

        if not question:
            continue

        if question=="/exit":
            break

        if question=="/help":
            print_help()
            continue

        if question=="/source":
            handle_source(rag)
            continue

        if question=="/clear":
            rag.memory.clear()

            print("\nMemory cleared.\n")
            continue


        result=rag.answer(question)

        print()
        print("Assistant : ")
        print(result["answer"])

        if result["citations"]:
            print()
            print("Sources : ")
            print(rag.formate_citations(result["citations"]))
            print()

if __name__ == "__main__":
    main()