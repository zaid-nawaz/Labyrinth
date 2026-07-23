from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from services.retrieval import get_retriever
from chains.prompts import prompt
from services.llm import llm
from chains.parsers import parser
from utils.utility import format_docs, format_timestamp


def rag_chain(video_id: str):

    retriever = get_retriever(video_id)

    parallel = RunnableParallel({
        "docs": retriever,
        "question": RunnablePassthrough()
    })

    parallel_chain = (
        parallel
        | RunnableLambda(lambda x: {
            "context": format_docs(x["docs"]),
            "timestamp": format_timestamp(x["docs"]),
            "question": x["question"]
        })
    )
    
    main_chain = parallel_chain | prompt | llm | parser
    
    return main_chain


