from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MEMORY_DIR = Path("memory")

INDEX_PATH = MEMORY_DIR / "memory.index"
METADATA_PATH = MEMORY_DIR / "memory_metadata.json"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)


# --------------------------------------------------
# Create or load memory store
# --------------------------------------------------

if INDEX_PATH.exists() and METADATA_PATH.exists():

    index = faiss.read_index(
        str(INDEX_PATH)
    )

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        memories = json.load(f)

else:

    embedding_dimension = 384

    index = faiss.IndexFlatL2(
        embedding_dimension
    )

    memories = []


# --------------------------------------------------
# Save memory store
# --------------------------------------------------

def save_memory_store():

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memories,
            f,
            indent=2,
            ensure_ascii=False
        )


# --------------------------------------------------
# Add memory
# --------------------------------------------------

def add_memory(text, memory_type="general"):

    embedding = embedding_model.encode(
        [text],
        convert_to_numpy=True
    ).astype("float32")

    index.add(embedding)

    memories.append({
        "text": text,
        "memory_type": memory_type
    })

    save_memory_store()


# --------------------------------------------------
# Search memory
# --------------------------------------------------

def search_memory(query, k=5):

    if index.ntotal == 0:
        return []

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    k = min(k, index.ntotal)

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for idx, distance in zip(
        indices[0],
        distances[0]
    ):

        result = memories[idx].copy()

        result["distance"] = float(distance)

        results.append(result)

    return results
