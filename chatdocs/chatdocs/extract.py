from pathlib import Path

from pypdf import PdfReader
from docx import Document

def extract_pdf(file_path:str):

    reader=PdfReader(file_path)

    source=Path(file_path).name

    documents=[]

    for page_num,page in enumerate(reader.pages, start=1):
        text=page.extract_text()

        if not text:
            continue

        text=text.strip()

        if not text:
            continue

        documents.append({
            "source":source,
            "page":page_num,
            "text":text
        })
    return documents


def extract_docx(file_path:str):

    document=Document(file_path)
    source=Path(file_path).name

    documents=[]

    section_num=1

    for para in document.paragraphs:

        text=para.text

        if not text:
            continue

        text=text.strip()

        if not text:
            continue

        documents.append({
            "source":source,
            "page":section_num,
            "text":text
        })
        section_num+=1
    return documents



def extract_document(file_path:str):

    suffix=Path(file_path).suffix.lower()

    if suffix==".pdf":
        return extract_pdf(file_path)

    if suffix==".docx":
        return extract_docx(file_path)

    raise ValueError(f"Unsupported file type: " f"{suffix}")



def find_documents(docs_dir:str):

    docs_path=Path(docs_dir)

    supported=[]

    for file in docs_path.rglob("*"):

        if file.suffix.lower() in {".pdf",".docx"}:
            supported.append(str(file))

    return supported


def extract_with_stats(
    file_path: str
):

    documents = extract_document(
        file_path
    )

    total_chars = sum(
        len(doc["text"])
        for doc in documents
    )

    return {
        "documents": documents,
        "count": len(documents),
        "characters": total_chars
    }