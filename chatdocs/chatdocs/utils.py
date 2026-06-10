import hashlib
from pathlib import Path

def calculate_file_hash(
    file_path: str
) -> str:

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as f:

        while chunk := f.read(8192):

            sha256.update(chunk)

    return sha256.hexdigest()



def ensure_directory(
    path: str
):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


def generate_chunk_id(source:str, page: int, chunk_index: int):

    raw=(
        f"{source}|"
        f"{page}|"
        f"{chunk_index}"
    )

    return hashlib.sha256(raw.encode("utf-8")).hexdigest()