from fastapi import FastAPI
from api.ingest import ingestion
from api.query import query

app = FastAPI()

@app.get('/')
def home():
    return {'message' : 'youtube rag pipeline'}

@app.get('/health')
def health_check():
    return {
        'status' : 'OK'
    }

app.include_router(ingestion)
app.include_router(query)



    