# Sample Queries

Run `python scripts/run_samples.py` from the `backend/` folder (or `make
samples` from the repo root) to reproduce these against your own key. To
capture the real output for the submission:

```bash
cd backend
python scripts/run_samples.py > ../docs/sample_output.txt
```

| # | Question | What to expect |
|---|----------|----------------|
| 1 | What is Agentic AI? | Definition from the intro section (~pages 7–10). |
| 2 | How is Agentic AI different from traditional generative AI? | Reactive vs. proactive contrast. |
| 3 | What are the main components of an Agentic AI system? | The "Anatomy of an Agentic AI System" section. |
| 4 | What is a multi-agent system? | From the Multi-Agent Systems section. |
| 5 | What are some practical applications of Agentic AI? | Use cases from the applications section. |
| 6 | How can an organization assess its readiness for Agentic AI? | From the "Your Readiness" section. |
| 7 | What is the capital of France? | **Not in the eBook** → the bot says it doesn't know. Proves grounding. |

### Example response from `POST /api/chat`

```json
{
  "question": "What is Agentic AI?",
  "answer": "Agentic AI refers to systems that ... (grounded in the eBook)",
  "confidence": 0.61,
  "chunks": [
    { "text": "Agentic AI is ...", "page": 8, "score": 0.63 },
    { "text": "Unlike reactive tools ...", "page": 9, "score": 0.59 }
  ]
}
```
