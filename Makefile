.PHONY: install ingest run samples test

# all backend commands run from the backend/ folder
install:
	cd backend && pip install -e ".[dev]"

ingest:
	cd backend && python scripts/ingest.py

run:
	cd backend && uvicorn app.main:app --reload

samples:
	cd backend && python scripts/run_samples.py

test:
	cd backend && pytest -q
