from typing import Any

import numpy as np
from numpy.typing import NDArray
from langchain_core.documents import Document

from vector_store.vector_storage import vector_store


Embedding = NDArray[Any]


def cosine_similarity(
    vec1: Embedding,
    vec2: Embedding,
) -> float:
    dot_product = np.dot(vec1, vec2)

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def semantic_search(
    query: str,
    video_id: str,
    k: int = 4,
) -> list[Document]:

    # 1. Convert the query into an embedding
    query_embedding = vector_store._embedding_function.embed_query(query)

    # 2. Get all chunks belonging to this video
    results = vector_store.get(
        where={"video_id": video_id},
        include=["documents", "metadatas", "embeddings"],
    )

    documents = results["documents"]
    metadatas = results["metadatas"]
    embeddings = results["embeddings"]

    # 3. Calculate similarity between query and every chunk
    scored_documents = []

    for document, metadata, embedding in zip(
        documents,
        metadatas,
        embeddings,
    ):
        similarity = cosine_similarity(
            np.array(query_embedding),
            np.array(embedding),
        )

        scored_documents.append(
            (similarity, document, metadata)
        )

    # 4. Sort highest similarity first
    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True,
    )

    # 5. Return top-K Documents
    return [
        Document(
            page_content=document,
            metadata={
                **metadata,
                "score": score,
            },
        )
        for score, document, metadata in scored_documents[:k]
    ]