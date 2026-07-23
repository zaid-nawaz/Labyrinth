from pydantic import BaseModel, Field
from typing import Annotated

class UserInput(BaseModel):
    
    video_id : Annotated[str, Field(..., description="video id of the video")]
    query : Annotated[str, Field(..., description="query about the youtube video")]
    