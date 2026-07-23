

from vector_store.vector_storage import vector_store

def retriever_pipeline(video_id : str):

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k" : 1, 
            "filter" : {"video_id" : video_id}
            }
        )
    
    return retriever
    
    
    