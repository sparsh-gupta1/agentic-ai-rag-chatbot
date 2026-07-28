"""
PDF -> text -> chunks -> embeddings -> Chroma.
Run through script entrypoint via  python scripts/ingest.py
"""
import requests
from pypdf import PdfReader

from app import config
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts
from app.rag import vector_store

EMBED_BATCH = 64  #chunks per API call


def download_pdf():
    if config.PDF_PATH.exists():
        print(f"PDF already present at {config.PDF_PATH}")
        return
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading eBook from {config.PDF_URL} ...")
    resp = requests.get(config.PDF_URL, timeout=60)
    resp.raise_for_status()
    config.PDF_PATH.write_bytes(resp.content)
    print(f"Saved {len(resp.content) // 1024} KB")


def read_pages():
    #Return [(page_number, text), ...], skip pages with no text
    reader = PdfReader(str(config.PDF_PATH))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append((i, text))
    print(f"Extracted text from {len(pages)} pages")
    return pages


def build_chunks(pages):
    #Turn pages into chunk records, keeping page num as metadata so we can cite it in answers
    records = []
    for page_num, text in pages:
        for j, chunk in enumerate(chunk_text(text)):
            records.append({
                "id": f"p{page_num}-c{j}",
                "text": chunk,
                "page": page_num,
            })
    print(f"Built {len(records)} chunks")
    return records


def run_ingest():
    download_pdf()
    pages = read_pages()
    records = build_chunks(pages)

    collection = vector_store.reset_collection()

    for i in range(0, len(records), EMBED_BATCH):
        part = records[i:i + EMBED_BATCH]
        vectors = embed_texts([r["text"] for r in part])
        collection.add(
            ids=[r["id"] for r in part],
            embeddings=vectors,
            documents=[r["text"] for r in part],
            metadatas=[{"page": r["page"]} for r in part],
        )
        print(f"  stored {min(i + EMBED_BATCH, len(records))}/{len(records)}")

    print(f"Done. Vector store ready at {config.CHROMA_DIR}")
