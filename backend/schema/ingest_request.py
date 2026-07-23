from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Annotated

class YoutubeURL(BaseModel):
    url : Annotated[HttpUrl, Field(..., description="youtube video url")]

    @field_validator("url")
    @classmethod
    def validate_youtube(cls, value: HttpUrl):
        if value.host not in {"youtube.com", "www.youtube.com", "youtu.be"}:
            raise ValueError("URL must be a YouTube URL")
        return value