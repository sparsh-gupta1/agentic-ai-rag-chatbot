#wrapper around the OpenAI embeddings
from functools import lru_cache

from openai import OpenAI

from app import config


@lru_cache(maxsize=1)
def _client():
    return OpenAI(api_key=config.OPENAI_API_KEY)


def embed_texts(texts):
    #Embed a list of strings, returning a list of vectors.
    #OpenAI takes a batch in one, which is far faster than one req/chunk.
    resp = _client().embeddings.create(model=config.EMBED_MODEL, input=texts)
    return [item.embedding for item in resp.data]


def embed_query(text):
    """Embed a single query string."""
    return embed_texts([text])[0]
