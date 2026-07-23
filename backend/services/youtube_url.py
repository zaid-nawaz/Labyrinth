from schema.ingest_request import YoutubeURL
from urllib.parse import parse_qs

def extract_video_id(data : YoutubeURL) -> str:
    
    youtube_url = data.url

    params = parse_qs(youtube_url.query)

    video_id = params["v"][0]
    
    return video_id