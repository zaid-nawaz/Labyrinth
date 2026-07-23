from app import app
from schema.ingest_request import YoutubeURL
from services.youtube_url import extract_video_id


@app.post('/ingest')
def ingestion(data : YoutubeURL):
    
    video_id = extract_video_id(data)

    return {"video_id" : video_id}