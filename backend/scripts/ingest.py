"""Build the vector store:  python scripts/ingest.py  (run from backend/)"""
from app.rag.ingestion import run_ingest

if __name__ == "__main__":
    run_ingest()
