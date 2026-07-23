from pydantic import BaseModel, Field
from typing import List

class QueryResponse(BaseModel):

    content : str = Field(description='content to show')
    offset : List[int] = Field(description='used for timestamp')