import json

def format_docs(retrieved_docs) -> str:
    context_parts = []

    for doc in retrieved_docs:

        segments = json.loads(
            doc.metadata.get("segments", "[]")
        )

        for segment in segments:
            context_parts.append(
                f"[{segment['offset']}] {segment['text']}"
            )

    return "\n".join(context_parts)

def format_timestamp(retrieved_docs) -> list[int]:
    timestamps = []

    for doc in retrieved_docs:
        segments = json.loads(
            doc.metadata.get("segments", "[]")
        )

        for segment in segments:
            timestamps.append(segment["offset"])
            
    print("TIMESTAMPS:", timestamps)

    return timestamps