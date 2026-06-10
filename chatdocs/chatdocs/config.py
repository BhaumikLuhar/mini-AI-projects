import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    GITHUB_TOKEN = os.getenv(
        "GITHUB_API_KEY"
    )

    MODEL = os.getenv(
        "MODEL2",
        "anthropic/claude-sonnet-4"
    )

    TOP_K = int(
        os.getenv(
            "TOP_K",
            "5"
        )
    )

    CHROMA_PATH = os.getenv(
        "CHROMA_PATH",
        "./chroma_data"
    )

    COLLECTION_NAME = os.getenv(
        "COLLECTION_NAME",
        "company_docs"
    )

    CHUNK_SIZE = int(
        os.getenv(
            "CHUNK_SIZE",
            "500"
        )
    )

    CHUNK_OVERLAP = int(
        os.getenv(
            "CHUNK_OVERLAP",
            "75"
        )
    )

    RELEVANCE_THRESHOLD = float(
        os.getenv(
            "RELEVANCE_THRESHOLD",
            "1.0"
        )
    )

    DENSE_WEIGHT = float(
        os.getenv(
            "DENSE_WEIGHT",
            "0.7"
        )
    )

    BM25_WEIGHT = float(
        os.getenv(
            "BM25_WEIGHT",
            "0.3"
        )
    )