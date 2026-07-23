from pydantic import BaseModel, Field

class output(BaseModel):

    content : str = Field(description='content to show')
    offset : int = Field(description='used for timestamp')