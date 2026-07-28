from fastapi import FastAPI
from api.ingest import router as ingest_router
from api.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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



    