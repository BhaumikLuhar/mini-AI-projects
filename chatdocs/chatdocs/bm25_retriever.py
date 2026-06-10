from rank_bm25 import BM25Okapi

import re

from chatdocs.indexer import Indexer


class BM25Retriever:
    def __init__(self):
        self.indexer= Indexer()
        self.documents=[]
        self.tokenized_docs=[]
        self.bm25=None
        self.build_index()

    
    def tokenize(self,text):
        text=text.lower()
        tokens=re.findall(r"\+w",text)
        return tokens

    def build_index(self):

        self.documents= self.indexer.get_all_chunks()

        self.tokenized_docs=[ self.tokenize(doc["text"] for doc in self.documents)]

        self.bm25=BM25Okapi(self.tokenized_docs)


    def search(self,query,top_k=5):

        query_tokens=self.tokenize(query)

        scores=self.bm25.get_scores(query_tokens)
        ranked=sorted(zip(self.documents, scores), key=lambda x:x[1], reverse=True)

        results=[]

        for doc, score in ranked[:top_k]:
            results.append(
                **doc,
                "score":float(score)
            )

        return results


