# Architecture

## Overview

The project is split into a **backend** (FastAPI + the RAG logic) and a
**frontend** (a static web UI that calls the backend over HTTP).

Two stages run inside the backend: an offline **ingestion** step that turns the
eBook into a searchable vector store, and an online **RAG pipeline** (a
LangGraph) that answers questions against it.

```
 frontend/ (HTML + CSS + JS)
        |  POST /api/chat  { question }
        v
 ┌──────────────────────────── backend (FastAPI) ────────────────────────────┐
 │                                                                            │
 │   PDF (Agentic AI eBook)                                                   │
 │        |                                                                   │
 │   ingestion (once):  download → extract → chunk → embed → store            │
 │        v                                                                   │
 │   Chroma vector DB  (backend/chroma_db/)                                   │
 │        ^                                                                   │
 │        |  top-k similar chunks                                             │
 │   question ──► LangGraph:  retrieve → generate ──► answer + chunks + score │
 │                                                                            │
 └────────────────────────────────────────────────────────────────────────────┘
        |
        v  JSON { answer, confidence, chunks }
 frontend renders it
```

## Backend layout

```
backend/app/
├── config.py            settings + model names + paths (reads .env)
├── models.py            Pydantic request/response schemas
├── main.py              FastAPI app: /api/chat + serves the frontend
└── rag/
    ├── chunking.py      custom text splitter
    ├── embeddings.py    OpenAI embedding helper
    ├── vector_store.py  Chroma wrapper (add / query)
    ├── ingestion.py     download → extract → chunk → embed → store
    └── pipeline.py      the LangGraph RAG pipeline
```

## Ingestion (`app/rag/ingestion.py`)

1. **Download** the PDF into `backend/data/` (skipped if already present).
2. **Extract** text page by page with `pypdf`; empty pages are dropped.
3. **Chunk** each page (`app/rag/chunking.py`) into ~800-character windows with
   150 characters of overlap, breaking only on whitespace.
4. **Embed** each chunk with `text-embedding-3-small`, in batches of 64.
5. **Store** vectors + text + page number in a local Chroma collection using
   cosine distance.

## RAG pipeline (`app/rag/pipeline.py`)

A compiled LangGraph `StateGraph` with two nodes and a shared `State`
(`question`, `chunks`, `answer`, `confidence`):

- **retrieve** — embeds the question with the same model used at ingest time
  and asks Chroma for the `TOP_K` (default 4) nearest chunks. Cosine distance
  becomes a `1 - distance` similarity.
- **generate** — builds a prompt from the retrieved chunks and calls
  `gpt-4o-mini` at temperature 0. The system prompt restricts the model to the
  provided context and tells it to refuse when the answer isn't there.

`answer_question()` is the single public entrypoint the API layer calls.

## Grounding

Answers stay grounded two ways:

1. The model only ever sees the retrieved chunks — no other context.
2. The system prompt forbids outside knowledge and requires an "I don't know
   based on the eBook" when the context doesn't contain the answer.

The off-topic sample question ("What is the capital of France?") demonstrates
this.

## Confidence

Confidence is the mean similarity of the retrieved chunks (0–1). It's a
retrieval heuristic, not a calibrated probability: when even the closest chunks
score low, the book probably doesn't cover the question, and the UI flags it.

## Serving

`app/main.py` exposes `POST /api/chat` (validated by the Pydantic models in
`app/models.py`) and also mounts the `frontend/` directory as static files, so
`uvicorn app.main:app` serves the whole app — UI at `/`, API under `/api`,
interactive docs at `/docs`. CORS is enabled so the frontend can also be served
separately if desired.

## Swapping components

Because the vector store sits behind `app/rag/vector_store.py`, moving from
Chroma to Pinecone (or another DB) only means rewriting that one file. Model
names live in `app/config.py` and are overridable via environment variables.
