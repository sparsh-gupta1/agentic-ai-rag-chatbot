"""
Chroma vector store wrapper our vectorDB
Kept behind a small interface so the rest of the code doesn't care that Chroma is underneath - moving to Pinecone would only mean rewriting this file.
"""
import chromadb

from app import config


def _client():
    return chromadb.PersistentClient(path=str(config.CHROMA_DIR))


def reset_collection():
    #Drop and recreate collection. Called at the start of ingestion so re-running doesn't pile up duplicate chunks.
    client = _client()
    try:
        client.delete_collection(config.COLLECTION_NAME)
    except Exception:
        pass  # nothing to delete on a first run
    # cosine space matches OpenAI embeddings better than the default L2
    return client.create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def get_collection():
    #Open the existing collection (raises if ingestion hasn't run yet)
    return _client().get_collection(config.COLLECTION_NAME)


def query(embedding, top_k):
    #Return the closest chunks to embedding as a list of dicts with txt, page num, and a 0-1 simi. score
    res = get_collection().query(query_embeddings=[embedding], n_results=top_k)

    chunks = []
    for text, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        chunks.append({
            "text": text,
            "page": meta.get("page"),
            # chroma returns cosine *distance*; similarity is 1 - distance
            "score": round(1 - dist, 3),
        })
    return chunks
