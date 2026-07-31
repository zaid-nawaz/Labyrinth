from dotenv import load_dotenv
from langchain_core.documents import Document
from services.transcript import get_transcript
from vector_store.vector_storage import vector_store
import json


load_dotenv()

def is_video_ingested(vector_store, video_id: str) -> bool:

    result = vector_store.get(where={"video_id": video_id}, limit=1)

    return len(result["ids"]) > 0


def ingestion_engine(video_id: str):

    if is_video_ingested(vector_store=vector_store, video_id=video_id):
        return {"status": "already_ingested", "video_id" : video_id }

    data = get_transcript(video_id)

    docs = []
    chunk_text = ""
    start_offset = None
    end_offset = None
    CHUNK_SIZE=800
    
    chunk_segments = []

    for segment in data["content"]:
        if start_offset is None:
            start_offset = segment["offset"]

        end_offset = segment["offset"] + segment["duration"]

        chunk_text += " " + segment["text"]
        
        chunk_segments.append({
            "text" : segment["text"],
            "offset" : segment["offset"],
            "duration" : segment["duration"]
         })

        if len(chunk_text) >= CHUNK_SIZE:
            docs.append(
                Document(
                    page_content=chunk_text.strip(),
                    metadata={
                        "chunk_id": f"{video_id}_{start_offset}_{end_offset}",
                        "start_offset": start_offset,
                        "end_offset": end_offset,
                        "video_id": video_id,
                        "segments" : json.dumps(chunk_segments),
                    },
                )
            )

            chunk_text = ""
            start_offset = None
            end_offset = None
            chunk_segments = []

    # remaining text
    if chunk_text:
        docs.append(
            Document(
                page_content=chunk_text.strip(),
                metadata={
                    "chunk_id": f"{video_id}_{start_offset}_{end_offset}",
                    "start_offset": start_offset,
                    "end_offset": end_offset,
                    "video_id": video_id,
                    "segments": json.dumps(chunk_segments),
                },
            )
        )

    vector_store.add_documents(docs)

    return {"status": "ingested", "chunks": len(docs), "video_id" : video_id}