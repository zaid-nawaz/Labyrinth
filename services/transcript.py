import httpx
# import os
from config import SUPADATA_API_KEY

def get_transcript(video_id: str) -> dict:  # key is content  and content contains a list of dictionaries with keys as lang text offset duration

    response = httpx.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        params={"videoId": video_id},
        headers={"x-api-key": SUPADATA_API_KEY},
        timeout=60.0,
    )

    if response.status_code != 200:
        raise Exception(f"Supadata error: {response.status_code} - {response.text}")

    data = response.json()

    return data
    