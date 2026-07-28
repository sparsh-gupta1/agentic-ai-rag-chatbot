from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import config
from app.models import Query, Answer
from app.rag.pipeline import answer_question

app = FastAPI(title="Agentic AI eBook Chatbot", version="0.1.0")

# allow the frontend to call the API when it's served from a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=Answer)
def chat(query: Query):
    result = answer_question(query.question)
    return {
        "question": query.question,
        "answer": result["answer"],
        "confidence": result["confidence"],
        "chunks": result["chunks"],
    }


if config.FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(config.FRONTEND_DIR), html=True),
        name="frontend",
    )
