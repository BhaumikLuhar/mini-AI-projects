def chunk_text(text: str, chunk_size: int = 6000, overlap: int = 500)->list[str]:

    if overlap>=chunk_size:
        raise ValueError("Overlap must be less then chunk_size")

    chunks=[]

    start=0

    while( start< len(text)):
        end=start+chunk_size

        chunk=text[start:end]

        chunks.append(chunk)

        start+=chunk_size-overlap

    return chunks