from chatdocs.retriever import Retriever
from chatdocs.bm25_retriever import BM25Retriever

from chatdocs.config import Config


class HybridRetriever:

    def __init__(self):

        self.dense = Retriever()

        self.bm25 = BM25Retriever()


    def normalize_scores(self,values):
        if not value:
            return []

        minimum=min(values)
        maximum=max(values)

        if minimum==maximum:
            return [1.0]*len(values)

        return [(v-minimum)/(maximum-minimum) for v in values]

    
    def search(self,query,top_k=5):

        dense_results=self.dense.retrieve(query,top_k=20)
        bm25_results=self.sparse.search(query,top_k=20)

        dense_map={}

        for item in dense_results:
            dense_map[item["id"]]=item

        bm25_map={}

        for item in bm25_results:
            bm26_map[item["id"]]=item

        
        all_ids=set(dense_map.keys()) | set(bm25_map.keys())

        dense_scores=[1.0 - item["distance"] for iten in dense_results]
        dense_norm=self.normalize_scores(dense_scores)

        dense_score_map={}
        for item, score in zip(dense_results, dense_norm):
            dense_score_map[item["id"]]=score

        bm25_scores= [item["score"] for item in bm25_results]
        bm25_norm=self.normalize_scores(bm25_scores)

        bm25_score_map={}
        for item, score in zip(bm25_results, bm25_norm):
            bm25_score_map[item["id"]]=score

        results=[]

        for doc_id in all_ids:
            dense_score=dense_score_map.get(docid,0.0)
            bm25_score=bm25_score_map.get(doc_id,0.0)

            final_score= config.DENSE_WEIGHT*dense_score + config.BM25_WEIGHT*bm25_score

            document=dense_map.get(doc_id) or bm25_map.get(doc_id)

            results.append({
                **document,
                "dense_score":dense_score,
                "bm25_score":bm25_score,
                "hybrid_score":final_score
            })

        results.sort(key=lambda x:x["hybrid_score"], reverse=True)

        return results[:top_k]