"""
Unit tests for the chunker. These need no API key, so they run anywhere with a
plain `pytest`.
"""
from app.rag.chunking import chunk_text


def test_short_text_is_one_chunk():
    text = "Agentic AI is a system that acts on its own."
    chunks = chunk_text(text, size=800, overlap=150)
    assert chunks == [text]


def test_long_text_splits_into_multiple_chunks():
    text = "word " * 1000  # ~5000 chars
    chunks = chunk_text(text, size=800, overlap=150)
    assert len(chunks) > 1


def test_chunks_respect_size_roughly():
    text = "word " * 1000
    chunks = chunk_text(text, size=800, overlap=150)
    # allow a little slack since we only break on whitespace
    assert all(len(c) <= 900 for c in chunks)


def test_consecutive_chunks_overlap():
    # unique tokens so we can spot shared words at the seam
    text = " ".join(f"tok{i}" for i in range(400))
    chunks = chunk_text(text, size=200, overlap=60)
    shared = set(chunks[0].split()) & set(chunks[1].split())
    assert shared
    # the next chunk should start with a token carried over from the previous
    assert chunks[1].split()[0] in set(chunks[0].split())


def test_no_word_is_cut_in_half():
    text = "supercalifragilistic " * 100
    chunks = chunk_text(text, size=100, overlap=20)
    for c in chunks:
        for word in c.split():
            assert word == "supercalifragilistic"
