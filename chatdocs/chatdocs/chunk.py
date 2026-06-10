from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from chatdocs.utils import (
    generate_chunk_id
)

from chatdocs.config import Config


def create_splitter():

    return RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )


def chunk_document(document: dict):

    splitter = create_splitter()

    chunks = splitter.split_text(document["text"])

    chunk_records = []

    for index, chunk in enumerate(chunks):

        chunk_records.append({
            "id": generate_chunk_id(document["source"], document["page"], index),
            "source": document["source"],
            "page": document["page"],
            "chunk_index": index,
            "text": chunk
        })

    return chunk_records


def chunk_documents(documents: list[dict]):

    all_chunks = []

    for doc in documents:
        chunks = chunk_document(doc)

        all_chunks.extend(chunks)

    return all_chunks


def chunk_statistics(
    chunks: list[dict]
):

    if not chunks:

        return {
            "count": 0,
            "avg_length": 0
        }

    lengths = [
        len(chunk["text"])
        for chunk in chunks
    ]

    return {
        "count": len(chunks),
        "avg_length": (
            sum(lengths)
            / len(lengths)
        ),
        "max_length": max(lengths),
        "min_length": min(lengths)
    }


def build_metadata(chunk: dict):

    return {
        "source": chunk["source"],
        "page": chunk["page"],
        "chunk_index": chunk["chunk_index"]
    }


def prepare_chroma_payload(chunks: list[dict]):

    ids = [
        chunk["id"] for chunk in chunks
    ]

    documents = [
        chunk["text"] for chunk in chunks
    ]

    metadatas = [
        build_metadata(chunk) for chunk in chunks
    ]

    return {
        "ids": ids,
        "documents": documents,
        "metadatas": metadatas
    }
