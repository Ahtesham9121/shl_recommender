import pickle
from pathlib import Path

import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


FAISS_PATH = Path("data/embeddings/shl_faiss.index")
METADATA_PATH = Path("data/embeddings/shl_metadata.pkl")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class HybridSearchEngine:

    def __init__(self):

        self.model = SentenceTransformer(MODEL_NAME)

        self.index = faiss.read_index(str(FAISS_PATH))

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        self.documents = [
            record["search_text"]
            for record in self.metadata
        ]

        tokenized_docs = [
            doc.lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized_docs)

    def semantic_search(self, query, top_k=10):

        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx, distance in zip(indices[0], distances[0]):

            record = self.metadata[idx]

            results.append({
                "id": record["id"],
                "score": float(distance),
                "source": "semantic",
                "record": record
            })

        return results

    def keyword_search(self, query, top_k=10):

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for idx in ranked_indices:

            record = self.metadata[idx]

            results.append({
                "id": record["id"],
                "score": float(scores[idx]),
                "source": "keyword",
                "record": record
            })

        return results

    def hybrid_search(self, query, top_k=10):

        semantic_results = self.semantic_search(query)

        keyword_results = self.keyword_search(query)

        combined = {}

        for result in semantic_results + keyword_results:

            record_id = result["id"]

            if record_id not in combined:
                combined[record_id] = result
            else:
                combined[record_id]["score"] += result["score"]

        final_results = list(combined.values())

        final_results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        formatted = []

        for item in final_results[:top_k]:

            record = item["record"]

            formatted.append({
                "name": record["name"],
                "url": record["url"],
                "description": record["description"],
                "skills": record.get("skills", []),
                "test_types": record.get("test_types", []),
                "score": item["score"]
            })

        return formatted