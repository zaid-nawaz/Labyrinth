import math
import string
from collections import Counter, defaultdict

from nltk.stem import PorterStemmer
from langchain_core.documents import Document

from vector_store.vector_storage import vector_store


BM25_K1 = 1.5
BM25_B = 0.75


def preprocess_text(text: str) -> str:
    text = text.lower()
    return text.translate(
        str.maketrans("", "", string.punctuation)
    )


def tokenize_text(text: str) -> list[str]:
    text = preprocess_text(text)

    tokens = text.split()

    # Remove stopwords if you have a stopword file.
    # For now, keeping this empty makes the implementation
    # self-contained.
    valid_tokens = [
        token for token in tokens
        if token
    ]

    stemmer = PorterStemmer()

    return [
        stemmer.stem(token)
        for token in valid_tokens
    ]


class InvertedIndex:

    def __init__(self, documents: list[Document]):
        self.documents = documents

        # token -> set(document_id)
        self.index: defaultdict[str, set[int]] = defaultdict(set)

        # document_id -> Counter(token -> frequency)
        self.term_frequencies: dict[int, Counter[str]] = defaultdict(Counter)

        # document_id -> number of tokens
        self.doc_lengths: dict[int, int] = {}

        self.build()

    def build(self) -> None:

        for doc_id, document in enumerate(self.documents):

            tokens = tokenize_text(
                document.page_content
            )

            # Inverted index
            for token in set(tokens):
                self.index[token].add(doc_id)

            # Term frequencies
            self.term_frequencies[doc_id].update(tokens)

            # Document length
            self.doc_lengths[doc_id] = len(tokens)

    def get_tf(
        self,
        doc_id: int,
        term: str,
    ) -> int:

        return self.term_frequencies[doc_id][term]

    def get_idf(
        self,
        term: str,
    ) -> float:

        document_count = len(self.documents)

        term_document_count = len(
            self.index.get(term, set())
        )

        return math.log(
            (document_count + 1)
            / (term_document_count + 1)
        )

    def get_bm25_idf(
        self,
        term: str,
    ) -> float:

        document_count = len(self.documents)

        term_document_count = len(
            self.index.get(term, set())
        )

        return math.log(
            (
                document_count
                - term_document_count
                + 0.5
            )
            /
            (
                term_document_count
                + 0.5
            )
            + 1
        )

    def get_average_document_length(self) -> float:

        if not self.doc_lengths:
            return 0.0

        return (
            sum(self.doc_lengths.values())
            / len(self.doc_lengths)
        )

    def get_bm25_tf(
        self,
        doc_id: int,
        term: str,
        k1: float = BM25_K1,
        b: float = BM25_B,
    ) -> float:

        tf = self.get_tf(doc_id, term)

        document_length = self.doc_lengths.get(
            doc_id,
            0,
        )

        average_document_length = (
            self.get_average_document_length()
        )

        if average_document_length == 0:
            return 0.0

        length_normalization = (
            1
            - b
            + b
            * (
                document_length
                / average_document_length
            )
        )

        return (
            tf * (k1 + 1)
        ) / (
            tf
            + k1 * length_normalization
        )

    def bm25(
        self,
        doc_id: int,
        term: str,
    ) -> float:

        tf_component = self.get_bm25_tf(
            doc_id,
            term,
        )

        idf_component = self.get_bm25_idf(
            term,
        )

        return tf_component * idf_component

    def search(
        self,
        query: str,
        k: int = 4,
    ) -> list[Document]:

        query_tokens = tokenize_text(query)

        scores: dict[int, float] = {}

        # Calculate BM25 score for every document
        for doc_id in range(len(self.documents)):

            score = 0.0

            for token in query_tokens:

                score += self.bm25(
                    doc_id,
                    token,
                )

            scores[doc_id] = score

        # Highest BM25 score first
        ranked_documents = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []

        for doc_id, score in ranked_documents[:k]:

            document = self.documents[doc_id]

            # Copy metadata so we don't mutate
            # the original Document
            metadata = {
                **document.metadata,
                "score": score,
            }

            results.append(
                Document(
                    page_content=document.page_content,
                    metadata=metadata,
                )
            )

        return results
    
    
def keyword_search(
    query: str,
    video_id: str,
    k: int = 4,
) -> list[Document]:

    # Get all chunks for this video
    results = vector_store.get(
        where={"video_id": video_id},
        include=["documents", "metadatas"],
    )

    documents = []

    for text, metadata in zip(
        results["documents"],
        results["metadatas"],
    ):
        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    # Build BM25 index over this video's chunks
    index = InvertedIndex(documents)

    # Search
    return index.search(
        query=query,
        k=k,
    )