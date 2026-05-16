import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


INPUT_PATH = Path("data/enriched/enriched_catalog.json")

FAISS_PATH = Path("data/embeddings/shl_faiss.index")
METADATA_PATH = Path("data/embeddings/shl_metadata.pkl")


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_catalog():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_model():
    print("Loading embedding model...")
    return SentenceTransformer(MODEL_NAME)


def build_texts(catalog):
    texts = []

    for record in catalog:
        texts.append(record["search_text"])

    return texts


def create_embeddings(model, texts):
    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def save_faiss(index):
    faiss.write_index(index, str(FAISS_PATH))


def save_metadata(catalog):
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(catalog, f)


if __name__ == "__main__":
    catalog = load_catalog()

    model = load_model()

    texts = build_texts(catalog)

    embeddings = create_embeddings(model, texts)

    index = create_faiss_index(embeddings)

    save_faiss(index)

    save_metadata(catalog)

    print("FAISS index saved.")
    print("Metadata saved.")
    print("Embedding pipeline complete.")