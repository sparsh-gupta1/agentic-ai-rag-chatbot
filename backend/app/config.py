import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# parents[1] is the backend/ dir
BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
DATA_DIR = BACKEND_ROOT / "data"
CHROMA_DIR = BACKEND_ROOT / "chroma_db"
FRONTEND_DIR = REPO_ROOT / "frontend"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

# number of chunks per question
TOP_K = int(os.getenv("TOP_K", "4"))

# knowledge base
PDF_URL = "https://konverge.ai/pdf/Ebook-Agentic-AI.pdf"
PDF_PATH = DATA_DIR / "Ebook-Agentic-AI.pdf"
COLLECTION_NAME = "agentic_ai_ebook"

# chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
