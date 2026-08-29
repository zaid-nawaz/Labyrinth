# Labyrinth

Chat with any YouTube video. Paste a link, and Labyrinth pulls the transcript, indexes it, and lets you ask questions about the video. Every answer comes back with clickable timestamps that jump the player straight to the relevant moment.

## How it works

1. **Ingest**: You submit a YouTube URL. The backend extracts the video ID, fetches the transcript via the [Supadata](https://supadata.ai) API, and splits it into ~800-character chunks (each chunk keeps its original timestamped segments in its metadata).
2. **Index**: Each chunk is embedded (OpenAI `text-embedding-3-large`, via OpenRouter) and stored in a local Chroma vector database. Videos already ingested are skipped.
3. **Ask**: When you send a question, Labyrinth runs a hybrid search over that video's chunks:
   - **Semantic search**: cosine similarity between the query embedding and every chunk embedding.
   - **BM25 keyword search**: a from-scratch inverted index + BM25 ranking (with Porter stemming).
   - Results from both are merged with **Reciprocal Rank Fusion (RRF)**.
4. **Answer**: The top chunks are passed to an LLM (`gpt-4o-mini` via OpenRouter) with a prompt that requires answers to be grounded strictly in the transcript. The model returns structured output: the answer text plus a list of supporting timestamps.
5. **Seek**: In the UI, each timestamp renders as a clickable chip. Clicking one seeks the embedded YouTube player to that moment.

## Tech stack

**Backend**
- FastAPI
- LangChain (`langchain-core`, `langchain-openai`)
- Chroma (vector store, persisted locally)
- OpenRouter (LLM + embeddings API)
- Supadata (YouTube transcript API)
- Hand-rolled BM25 / RRF hybrid retrieval

**Frontend**
- Next.js 16 (App Router) + React 19
- Tailwind CSS 4
- `react-youtube` for the embedded player
- Axios

## Project structure

```
backend/
  api/            FastAPI route handlers (/ingest, /query)
  chains/         LangChain prompt, output parser, and RAG chain
  schema/         Pydantic request/response models
  services/       Transcript fetching, ingestion pipeline, LLM client
    retrievers/   Semantic search, BM25 search, RRF fusion, hybrid search
  utils/          Formatting helpers
  vector_store/   Chroma vector store configuration
  app.py          FastAPI app entrypoint
  config.py       Environment variable loading

frontend/
  app/            Next.js App Router pages and global styles
  components/     Chat UI, video form, video player
  lib/            API client, timestamp formatting
  types/          Shared TypeScript types
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai) API key (used for both the LLM and embeddings)
- A [Supadata](https://supadata.ai) API key (used to fetch YouTube transcripts)

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install nltk  # required by the BM25 retriever; not currently pinned in requirements.txt
```

Create a `.env` file inside `backend/`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
SUPADATA_API_KEY=your_supadata_api_key
```

Run the API:

```bash
uvicorn app:app --reload
```

The backend starts at `http://localhost:8000`. The Chroma database is persisted to `backend/my_chroma_db/` and created automatically on first run.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app is available at `http://localhost:3000`. It expects the backend to be running at `http://localhost:8000` (configured in `frontend/lib/api.ts`).

## API

### `POST /ingest`

Ingests a YouTube video's transcript.

**Request**
```json
{ "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
```

**Response**
```json
{ "status": "ingested", "chunks": 12, "video_id": "VIDEO_ID" }
```
(`status` is `"already_ingested"` if the video was previously indexed.)

### `POST /query`

Asks a question about an ingested video.

**Request**
```json
{ "video_id": "VIDEO_ID", "query": "What does the speaker say about X?" }
```

**Response**
```json
{ "content": "The speaker explains that...", "offset": [12000, 45200] }
```

`offset` values are millisecond timestamps into the video, used by the frontend to render seekable timestamp chips.

### `GET /health`

Basic health check, returns `{ "status": "OK" }`.

## Notes

- CORS is currently restricted to `http://localhost:3000`; update `backend/app.py` if you deploy the frontend elsewhere.
- The vector store scopes retrieval by `video_id`, so each video's chunks are searched independently.
- `nltk` (used for stemming in the BM25 retriever) isn't listed in `requirements.txt`. Install it separately, and run `nltk.download('punkt')` if you hit a missing-corpus error.
