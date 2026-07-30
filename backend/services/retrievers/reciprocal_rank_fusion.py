from langchain_core.documents import Document


RRF_K = 60


def rrf_score(
    rank: int,
    k: int = RRF_K,
) -> float:
    return 1 / (k + rank)


def reciprocal_rank_fusion(
    bm25_results: list[Document],
    semantic_results: list[Document],
    k: int = RRF_K,
) -> list[Document]:

    rrf_scores = {}

    documents = {}

    # BM25 results
    for rank, document in enumerate(
        bm25_results,
        start=1,
    ):
        chunk_id = document.metadata["chunk_id"]

        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0.0

        rrf_scores[chunk_id] += rrf_score(
            rank,
            k,
        )

        documents[chunk_id] = document

    # Semantic results
    for rank, document in enumerate(
        semantic_results,
        start=1,
    ):
        chunk_id = document.metadata["chunk_id"]

        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0.0

        rrf_scores[chunk_id] += rrf_score(
            rank,
            k,
        )

        documents[chunk_id] = document

    # Highest RRF score first
    ranked_chunks = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    results = []

    for chunk_id, score in ranked_chunks:

        document = documents[chunk_id]

        results.append(
            Document(
                page_content=document.page_content,
                metadata={
                    **document.metadata,
                    "rrf_score": score,
                },
            )
        )

    return results