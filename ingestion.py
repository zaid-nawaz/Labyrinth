from dotenv import load_dotenv
from langchain_core.documents import Document

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from fastapi.responses import JSONResponse
from vector_store.vector_storage import vector_store

load_dotenv()

dummy_transcript = {
    "lang": "en",
    "availableLangs": ["en"],
    "content": [
        {
            "lang": "en",
            "text": "Welcome everyone. Today we're going to talk about machine learning fundamentals.",
            "offset": 0,
            "duration": 5200,
        },
        {
            "lang": "en",
            "text": "Many beginners jump straight into deep learning without understanding the basics.",
            "offset": 5200,
            "duration": 4800,
        },
        {
            "lang": "en",
            "text": "You should first understand linear regression, classification, and evaluation metrics.",
            "offset": 10000,
            "duration": 6100,
        },
        {
            "lang": "en",
            "text": "Once you're comfortable with those concepts, neural networks become much easier to understand.",
            "offset": 16100,
            "duration": 6700,
        },
        {
            "lang": "en",
            "text": "Let's now build our first model using Python and scikit-learn.",
            "offset": 22800,
            "duration": 5400,
        },
        {
            "lang": "en",
            "text": "We'll split our dataset into training and testing sets before fitting the model.",
            "offset": 28200,
            "duration": 6200,
        },
        {
            "lang": "en",
            "text": "Finally, we'll evaluate the model using accuracy, precision, recall, and F1 score.",
            "offset": 34400,
            "duration": 7000,
        },
        {
            "lang": "en",
            "text": "In the next lecture we'll explore decision trees and random forests in more detail.",
            "offset": 41400,
            "duration": 6300,
        },
    ],
}


def get_transcript(
    video_id: str,
) -> dict:  # key is content  and content contains a list of dictionaries with keys as lang text offset duration
    # SUPADATA_API_KEY = os.environ.get("SUPADATA_API_KEY")

    # response = httpx.get(
    #     "https://api.supadata.ai/v1/youtube/transcript",
    #     params={"videoId": video_id},
    #     headers={"x-api-key": SUPADATA_API_KEY},
    #     timeout=60.0,
    # )

    # if response.status_code != 200:
    #     raise Exception(f"Supadata error: {response.status_code} - {response.text}")

    # data = response.json()

    # return data
    return dummy_transcript


def is_video_ingested(vector_store, video_id: str) -> bool:

    result = vector_store.get(where={"video_id": video_id}, limit=1)

    return len(result["ids"]) > 0


def ingestion_engine(video_id: str):

    if is_video_ingested(vector_store=vector_store, video_id=video_id):
        return {"status": "already_ingested"}

    data = get_transcript(video_id)

    docs = []
    chunk_text = ""
    start_offset = None
    end_offset = None
    CHUNK_SIZE=800

    for segment in data["content"]:
        if start_offset is None:
            start_offset = segment["offset"]

        end_offset = segment["offset"] + segment["duration"]

        chunk_text += " " + segment["text"]

        if len(chunk_text) >= CHUNK_SIZE:
            docs.append(
                Document(
                    page_content=chunk_text.strip(),
                    metadata={
                        "start_offset": start_offset,
                        "end_offset": end_offset,
                        "video_id": video_id,
                    },
                )
            )

            chunk_text = ""
            start_offset = None
            end_offset = None

    # remaining text
    if chunk_text:
        docs.append(
            Document(
                page_content=chunk_text.strip(),
                metadata={
                    "start_offset": start_offset,
                    "end_offset": end_offset,
                    "video_id": video_id,
                },
            )
        )

    vector_store.add_documents(docs)

    return {"status": "ingested", "chunks": len(docs), "video_id" : video_id}
