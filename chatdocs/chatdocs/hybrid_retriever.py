from chatdocs.retriever import Retriever
from chatdocs.bm25_retriever import BM25Retriever

from chatdocs.config import Config
from chatdocs.utils import (
    generate_chunk_id
)


class HybridRetriever:

    def __init__(self):

        self.dense = Retriever()

        self.bm25 = BM25Retriever()
        self.indexer = self.dense.indexer

    def normalize_scores(self, values):
        if not values:
            return []

        minimum = min(values)
        maximum = max(values)

        if minimum == maximum:
            if maximum == 0:
                return [0.0] * len(values)

            return [1.0]*len(values)

        return [(v-minimum)/(maximum-minimum) for v in values]

    def build_context(self, chunks):

        return self.dense.build_context(chunks)

    def extract_citations(self, chunks):

        return self.dense.extract_citations(chunks)

    def best_distance(self, chunks):

        dense_distances = [
            chunk.get("distance")
            for chunk in chunks
            if chunk.get("distance") is not None
        ]

        if not dense_distances:
            return None

        return min(dense_distances)

    def has_results(self, chunks):

        if not chunks:
            return False

        best_distance = self.best_distance(chunks)

        if (
            best_distance is not None
            and best_distance <= Config.RELEVANCE_THRESHOLD
        ):
            return True

        return any(
            chunk.get("bm25_score", 0.0) > 0
            for chunk in chunks
        )

    def retrieve_chunks(self, query, top_k=None):

        if top_k is None:
            top_k = Config.TOP_K

        dense_results = self.dense.retrieve_chunks(query, top_k=20)
        bm25_results = self.bm25.search(query, top_k=20)

        dense_map = {}
        for item in dense_results:
            item_id = item.get("id") or generate_chunk_id(
                item["source"],
                item["page"],
                item["chunk_index"]
            )
            item["id"] = item_id
            dense_map[item_id] = item

        bm25_map = {}
        for item in bm25_results:
            item_id = item.get("id") or generate_chunk_id(
                item["source"],
                item["page"],
                item["chunk_index"]
            )
            item["id"] = item_id
            bm25_map[item_id] = item

        all_ids = set(dense_map.keys()) | set(bm25_map.keys())

        dense_scores = [
            1.0 - float(item.get("distance") or 0.0)
            for item in dense_results
        ]
        dense_norm = self.normalize_scores(dense_scores)

        dense_score_map = {}
        for item, score in zip(dense_results, dense_norm):
            dense_score_map[item["id"]] = score

        bm25_scores = [
            float(item.get("score") or 0.0)
            for item in bm25_results
        ]
        bm25_norm = self.normalize_scores(bm25_scores)

        bm25_score_map = {}
        for item, score in zip(bm25_results, bm25_norm):
            bm25_score_map[item["id"]] = score

        results = []

        for doc_id in all_ids:
            dense_item = dense_map.get(doc_id)
            bm25_item = bm25_map.get(doc_id)
            document = dense_item or bm25_item

            if not document:
                continue

            dense_score = dense_score_map.get(doc_id, 0.0)
            bm25_score = bm25_score_map.get(doc_id, 0.0)

            results.append(
                {
                    **document,
                    "distance": dense_item.get("distance") if dense_item else None,
                    "dense_score": dense_score,
                    "bm25_score": bm25_score,
                    "hybrid_score": (
                        Config.DENSE_WEIGHT * dense_score
                        + Config.BM25_WEIGHT * bm25_score
                    ),
                }
            )

        results.sort(key=lambda x: x["hybrid_score"], reverse=True)

        return results[:top_k]

    def search(self, query, top_k=20):
        return self.retrieve_chunks(query, top_k=top_k)

    def retrieve_context(self, query, top_k=None):

        chunks = self.retrieve_chunks(query, top_k)

        context = self.build_context(chunks)

        citations = self.extract_citations(chunks)

        return {
            "chunks": chunks,
            "context": context,
            "citations": citations,
            "found": self.has_results(chunks),
            "best_distance": self.best_distance(chunks)
        }
