from chatdocs.indexer import (
    Indexer
)

from chatdocs.config import (
    Config
)


class Retriever:

    def __init__(self):

        self.indexer=Indexer()


    def retrieve(self, query, top_k=None):

        if top_k is None:
            top_k=Config.TOP_K

        return self.indexer.search(query,top_k)


    def build_context(self, chunks):

        context_parts=[]

        for chunk in chunks:
            block = (
                f"Source: {chunk['source']}\n"
                f"Page: {chunk['page']}\n\n"
                f"{chunk['text']}"
            )

            context_parts.append(block)

        return "\n\n------------------\n\n".join(context_parts)
    

    def extract_citations(self,chunks):

        citations=set()

        for chunk in chunks:

            citations.add(
                (
                    chunk["source"],
                    chunk["page"]
                )
            )

        return sorted(citations)
    
    def has_results(
        self,
        chunks
    ):

        if not chunks:

            return False

        best_distance = min(
            chunk["distance"]
            for chunk in chunks
        )

        return (
            best_distance
            <= Config.RELEVANCE_THRESHOLD
        )

    

    def retrieve_context(self,query,top_k=None):

        chunks=self.retrieve(query,top_k)

        context=self.build_context(chunks)

        citations= self.extract_citations(chunks)

        return {
            "chunks": chunks,
            "context": context,
            "citations": citations,
            "found": self.has_results(
                chunks
            ),
            "best_distance": self.best_distance(chunks)
        }
    
    def best_distance(self,chunks):
        if not chunks:
            return None
        
        return min(chunk["distance"] for chunk in chunks)
        