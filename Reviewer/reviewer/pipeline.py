from reviewer.chunk import chunk_text
from reviewer.extract import extract_text
from reviewer.models import ChunkAnalysis
from reviewer.prompts import CHUNK_ANALYSIS_PROMPT, FINAL_REVIEW_PROMPT
from reviewer.llm import validate_with_retry
import json
from reviewer.models import ReviewReport
import time


def analyze_chunk(chunk: str) -> ChunkAnalysis:

    prompt = (
        CHUNK_ANALYSIS_PROMPT
        .replace(
            "{chunk}",
            chunk
        )
    )

    return validate_with_retry(
        prompt,
        ChunkAnalysis
    )


def map_document(chunks:list[str])->list[ChunkAnalysis]:
    results=[]

    total=len(chunks)

    for idx,chunk in enumerate(chunks,start=1):
        print(
            f"[{idx}/{total}] "
            f"Analyzing chunk..."
        )

        result=analyze_chunk(chunk)

        results.append(result)

        time.sleep(1)

    return results


def prepare_document(
    file_path: str
):

    text = extract_text(
        file_path
    )

    chunks = chunk_text(
        text
    )

    analyses = map_document(
        chunks
    )

    report = reduce_document(
        analyses
    )


    return {
        "text": text,
        "chunks": chunks,
        "chunk_count": len(chunks),
        "analyses": analyses,
        "report": report
    }


def serialize_findings(analyses)->str:

    return json.dumps(
        [a.model_dump() for a in analyses], indent=2
    )

def reduce_document(
    analyses
) -> ReviewReport | None:

    findings = serialize_findings(
        analyses
    )

    prompt = (
        FINAL_REVIEW_PROMPT
        .replace(
            "{findings}",
            findings
        )
    )

    report = validate_with_retry(
        prompt,
        ReviewReport
    )

    return report


