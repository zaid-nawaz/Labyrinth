import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma  
load_dotenv()


vector_store = Chroma(
    embedding_function=OpenAIEmbeddings(
        model="openai/text-embedding-3-large",
        dimensions=1536,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    ),
    persist_directory='my_chroma_db',
    collection_name='videos_transcript_chunks_1536'
)