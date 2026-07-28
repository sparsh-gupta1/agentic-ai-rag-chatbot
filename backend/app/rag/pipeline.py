"""
LangGraph:  retrieve >> generate >> END
- retrieve: embed question, pull closest chunks from vectorDB
- generate: answer using ONLY those chunks, refusing when book doesn't cover it
entrypoint is answer_question();
"""
from typing import TypedDict, List

from openai import OpenAI
from langgraph.graph import StateGraph, END

from app import config
from app.rag import vector_store
from app.rag.embeddings import embed_query


class State(TypedDict):
    question: str
    chunks: List[dict]
    answer: str
    confidence: float


SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about the 'Agentic AI' "
    "eBook. Use ONLY the context provided. If the answer isn't in the context, "
    "say you don't know based on the eBook - do not use outside knowledge and "
    "do not guess. Be clear and concise, and cite the page number when useful."
)


def _llm():
    return OpenAI(api_key=config.OPENAI_API_KEY)


def retrieve(state: State) -> State:
    #Embed the question and fetch top-k chunks
    q_embed = embed_query(state["question"])
    state["chunks"] = vector_store.query(q_embed, config.TOP_K)
    return state


def generate(state: State) -> State:
    #Score confidence and ask LLM to answer from retrieved context
    chunks = state["chunks"]

    # confidence = average of retrieved chunks. If even the best
    # matches are far off, the book likely doesn't cover the question.
    state["confidence"] = (
        round(sum(c["score"] for c in chunks) / len(chunks), 3) if chunks else 0.0
    )

    context = "\n\n".join(f"[page {c['page']}] {c['text']}" for c in chunks)
    user_prompt = (
        f"Context from the eBook:\n{context}\n\n"
        f"Question: {state['question']}\n\n"
        "Answer using only the context above."
    )

    resp = _llm().chat.completions.create(
        model=config.CHAT_MODEL,
        temperature=0,  # deterministic + factual
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    state["answer"] = resp.choices[0].message.content.strip()
    return state


def build_graph():
    g = StateGraph(State)
    g.add_node("retrieve", retrieve)
    g.add_node("generate", generate)
    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "generate")
    g.add_edge("generate", END)
    return g.compile()


# compiled once at import; cheap to reuse across requests
_graph = build_graph()


def answer_question(question: str) -> dict:
    #Run one question through the graph and return a plain dict
    result = _graph.invoke({"question": question})
    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "chunks": result["chunks"],
    }
