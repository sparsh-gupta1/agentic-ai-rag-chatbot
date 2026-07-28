# Agentic AI eBook Chatbot

This is my submission for the AI Engineer intern task. It's a chatbot that
answers questions from the Agentic AI eBook by Konverge AI. It only answer
from the book — if something is not in the book, it says it doesn't know
instead of making up an answer.

I built it using RAG (Retrieval-Augmented Generation). The idea is simple:
first find the parts of the book that are related to the question, then give
those parts to the LLM and ask it to answer using only that.

## Tech I used

- Python
- LangGraph for the RAG pipeline
- Chroma as the vector database (the task allowed any vector DB, Chroma is free
  and runs locally so I didn't need a Pinecone account)
- OpenAI for the embeddings and the answers (text-embedding-3-small and
  gpt-4o-mini)
- FastAPI for the backend API
- HTML, CSS and JavaScript for a simple chat page

Each answer returns three things like the task asked: the final answer, the
context chunks it used (with page numbers), and a confidence score.

## Sample questions to try

- What is Agentic AI?
- How is Agentic AI different from generative AI?
- What are the main components of an Agentic AI system?
- What is a multi-agent system?
- What are some practical applications of Agentic AI?
- What is the capital of France?  (this one is not in the book, so it should
  say it doesn't know — that shows the answers are grounded)

## How it works (short version)

When you ask a question, the app turns your question into an embedding and
searches Chroma for the 4 most similar chunks from the book. Then it puts those
chunks into the prompt and asks the LLM to answer using only that context. The
system prompt tells the model not to use outside knowledge. The confidence
score is just the average similarity of the chunks it found.

I also wrote a few unit tests for the text chunking part.


## Notes / things I could improve

- The chunking is a simple fixed-size split. A smarter split based on headings
  would probably give better results.
- The confidence score is a simple similarity average, not a real probability.
- Right now every question is separate, there is no chat history yet.
