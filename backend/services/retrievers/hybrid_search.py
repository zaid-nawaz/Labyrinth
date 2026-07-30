from langchain_core.documents import Document

from .semantic_search import semantic_search
from .bm25_keyword_search import keyword_search
from .reciprocal_rank_fusion import reciprocal_rank_fusion


def hybrid_search(
    query: str,
    video_id: str,
    k: int = 4,
) -> list[Document]:
    
    candidate_k = 20

    # Retrieve candidates from both systems
    semantic_results = semantic_search(
        query=query,
        video_id=video_id,
        k=candidate_k
    )

    bm25_results = keyword_search(
        query=query,
        video_id=video_id,
        k=candidate_k,
    )

    # Fuse the ranked results
    fused_results = reciprocal_rank_fusion(
        bm25_results=bm25_results,
        semantic_results=semantic_results,
    )

    # Final top-K
    return fused_results[:k]