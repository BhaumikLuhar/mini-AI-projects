from dataclasses import dataclass


@dataclass
class DocumentChunk:

    source: str

    page: int

    text: str