from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

VECTOR_STORE_DIR = Path("vector_store")

INDEX_PATH = VECTOR_STORE_DIR / "acme_documents.index"
METADATA_PATH = VECTOR_STORE_DIR / "metadata.json"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# --------------------------------------------------
# Load vector store
# --------------------------------------------------

index = faiss.read_index(str(INDEX_PATH))

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)


# --------------------------------------------------
# Document Search Tool
# --------------------------------------------------

def document_search(query, k=5):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for idx, distance in zip(indices[0], distances[0]):

        result = metadata[idx].copy()

        result["distance"] = float(distance)

        results.append(result)

    return results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    query = "What are Acme Corp's current integration blockers?"

    results = document_search(query)

    for i, result in enumerate(results, start=1):

        print(f"\n{'=' * 70}")
        print(f"Result {i}")
        print(f"Source: {result['source']}")
        print(f"Type: {result['document_type']}")
        print(f"Distance: {result['distance']:.4f}")
        print("\n", result["text"])
