from fastapi import FastAPI
from api.ingest import router as ingest_router
from api.query import router as query_router

app = FastAPI()

@app.get('/')
def home():
    return {'message' : 'youtube rag pipeline'}

@app.get('/health')
def health_check():
    return {
        'status' : 'OK'
    }

app.include_router(ingest_router)
app.include_router(query_router)



    