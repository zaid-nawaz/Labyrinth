from fastapi import APIRouter
from schema.ingest_request import YoutubeURL
from services.youtube_url import extract_video_id
from services.ingestion import ingestion_engine

router = APIRouter()


@router.post('/ingest')
def ingestion(data : YoutubeURL):
    
    video_id = extract_video_id(data)
    
    result = ingestion_engine(video_id=video_id)

    return result