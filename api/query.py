from schema.query_request import UserInput
from app import app

@app.post("/query")
def query(data : UserInput):
    
    return {}