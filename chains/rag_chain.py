from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from services.retrieval import retriever_pipeline
from chains.prompts import prompt
from services.llm import llm
from chains.parsers import parser
from utils.utility import format_docs, format_timestamp


def rag_chain(video_id: str):

    retriever = retriever_pipeline(video_id)

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough(),
        'timestamp' : retriever | RunnableLambda(format_timestamp)
    })
    
    main_chain = parallel_chain | prompt | llm | parser
    
    return main_chain


