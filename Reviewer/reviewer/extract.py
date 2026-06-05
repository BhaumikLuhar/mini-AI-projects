from pathlib import Path
from pypdf import PdfReader

def extract_pdf_text(file_path: str)->str:

    reader=PdfReader(file_path)

    pages=[]

    for page in reader.pages:
        text=page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_txt_text(file_path: str)->str:

    with open(file_path,"r",encoding="utf-8")as f:
        return f.read()


def extract_text(file_path:str)->str:
    
    path=Path(file_path)

    suffix= path.suffix.lower()

    if suffix==".pdf":
        return extract_pdf_text(file_path)

    if suffix==".txt":
        return extract_txt_text(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")