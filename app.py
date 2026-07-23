from fastapi import FastAPI
from schema.youtube_url import YoutubeURL
from urllib.parse import parse_qs

app = FastAPI()

@app.get('/')
def home():
    return {'message' : 'youtube rag pipeline'}

@app.get('/health')
def health_check():
    return {
        'status' : 'OK'
    }

@app.post('/ingest')
def ingestion(data : YoutubeURL):

    youtube_url = data.url

    params = parse_qs(youtube_url.query)

    video_id = params["v"][0]

    return {"video_id" : video_id}



    