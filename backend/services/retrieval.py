from vector_store.vector_storage import vector_store

def get_retriever(video_id : str):

    

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k" : 4, 
            "filter" : {"video_id" : video_id}
            }
        )
    
    return retriever
    
    
    