from schema.query_request import UserInput
from fastapi import APIRouter
from chains.rag_chain import rag_chain
from schema.query_response import QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(data : UserInput):
    
    question = data.query
    video_id = data.video_id
    
    main_chain = rag_chain(video_id=video_id)
    
    result = main_chain.invoke(question)
    
    return result