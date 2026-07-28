#Text chunking: We break on whitespace (no mid-word) so chunks stay readable.
from app import config


def chunk_text(text, size=None, overlap=None):
    #Split text to size chunks with overlap chars b/w consecutive chunks and Return a list[str]
    size = size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    words = text.split()
    chunks = []
    current = []
    length = 0

    for word in words:
        current.append(word)
        length += len(word) + 1
        if length >= size:
            chunks.append(" ".join(current))
            current, length = _tail(current, overlap)

    if current:
        chunks.append(" ".join(current))
    return chunks


def _tail(words, overlap):
    #Return trailing words that fit within overlap chars, so next chunk starts with a bit of prev one
    back = []
    back_len = 0
    for w in reversed(words):
        back_len += len(w) + 1
        back.insert(0, w)
        if back_len >= overlap:
            break
    return back, back_len
