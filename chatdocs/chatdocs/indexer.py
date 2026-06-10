import chromadb

from sentence_transformers import (
    SentenceTransformer
)
from chatdocs.chunk import (
    prepare_chroma_payload
)
from chatdocs.config import Config

from pathlib import Path

from chatdocs.extract import (
    extract_document
)

from chatdocs.chunk import (
    chunk_documents
)

from chatdocs.utils import (
    calculate_file_hash
)

from chatdocs.indexing_state import (
    StateManager
)

from chatdocs.extract import (
    find_documents
)

class Indexer:

    def __init__(self):
        self.client=chromadb.PersistentClient(path=Config.CHROMA_PATH)

        self.collection=self.client.get_or_create_collection(Config.COLLECTION_NAME)

        self.embedding_model=SentenceTransformer("all-MiniLM-L6-v2")

        self.state=StateManager()

    def count(self):
        return self.collection.count()

    def add_chunks(self,chunks):

        if not chunks:
            return
        
        payload=prepare_chroma_payload(chunks)

        embeddings=self.embedding_model.encode(
            payload["documents"],
            show_progress_bar=True
        )

        self.collection.add(
            ids=payload["ids"],
            documents=payload["documents"],
            metadatas=payload["metadatas"],
            embeddings=embeddings.tolist()
        )


    def search(self,query,top_k=5):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents=results.get("documents")
        metadatas=results.get("metadatas")
        distances=results.get("distances")
        matches=[]

        if not documents:
            return []
        for i, doc in enumerate(documents[0]):
            matches.append(
                {
                    "text": doc,
                    "source": metadatas[0][i]["source"] if metadatas else None,
                    "page": metadatas[0][i]["page"] if metadatas else None,
                    "chunk_index": metadatas[0][i]["chunk_index"] if metadatas else None,
                    "distance" : distances[0][i] if distances else None
                }
            )

        return matches
    

    def delete_source(self,source_name):
        results=self.collection.get(
            where={
                "source": source_name
            }
        )

        if results["ids"]:
            self.collection.delete(ids=results["ids"])


    def list_sources(self):

        results=self.collection.get()

        sources=set()

        metas=results.get("metadatas")
        if not metas:
            return set()

        for meta in metas:
            sources.add(meta["source"])

        return sorted(sources)
    

    def file_needs_indexing(self,file_path):

        source=Path(file_path).name

        current_hash=calculate_file_hash(file_path)

        saved_hash=self.state.get_hash(source)

        return current_hash!=saved_hash
    

    def index_file(self, file_path):

        documents=extract_document(file_path)

        chunks=chunk_documents(documents)

        source_name=Path(file_path).name

        self.delete_source(source_name)

        self.add_chunks(chunks)

        file_hash=calculate_file_hash(file_path)

        self.state.update_file(source_name, file_hash)


    def index_folder(self,docs_dir):

        files=find_documents(docs_dir)

        indexed=0
        skipped=0

        for file_path in files:
            if not self.file_needs_indexing(file_path):
                print(
                    f"Skipping "
                    f"{Path(file_path).name}"
                )
                skipped+=1
                continue

            print(
                f"Indexing "
                f"{Path(file_path).name}"
            )

            self.index_file(file_path)
            indexed+=1

        return {
            "indexed": indexed,
            "skipped": skipped,
            "total": len(files)
        }


    def get_all_chunks(self):
        results=self.collection.get(include=["documents","metadatas"])
        chunks=[]

        for doc, meta in zip(results["documents"],results["metadatas"]):

            chunks.append({
                "text":doc,
                **meta
            })

        return chunks

        