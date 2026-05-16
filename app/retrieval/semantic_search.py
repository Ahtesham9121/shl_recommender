import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


FAISS_PATH = Path("data/embeddings/shl_faiss.index")
METADATA_PATH = Path("data/embeddings/shl_metadata.pkl")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticSearchEngine:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

        self.index = faiss.read_index(str(FAISS_PATH))

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=5):

        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx, distance in zip(indices[0], distances[0]):

            record = self.metadata[idx]

            results.append({
                "score": float(distance),
                "name": record["name"],
                "url": record["url"],
                "description": record["description"],
                "skills": record.get("skills", []),
                "test_types": record.get("test_types", [])
            })

        return results