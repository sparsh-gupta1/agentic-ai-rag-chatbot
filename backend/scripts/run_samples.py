#Run the demo questions through the pipeline and print the results.
from app.rag.pipeline import answer_question

QUESTIONS = [
    "What is Agentic AI?",
    "How is Agentic AI different from traditional generative AI?",
    "What are the main components of an Agentic AI system?",
    "What is a multi-agent system?",
    "What are some practical applications of Agentic AI?",
    "How can an organization assess its readiness for Agentic AI?",
    "What is the capital of France?",  # out-of-scope on purpose
]


def main():
    for q in QUESTIONS:
        result = answer_question(q)
        print("=" * 72)
        print("Q:", q)
        print("-" * 72)
        print(result["answer"])
        print(f"\nconfidence: {result['confidence']}")
        print("context pages:", sorted({c["page"] for c in result["chunks"]}))
        print()


if __name__ == "__main__":
    main()
