#!/usr/bin/env bash
# Start script used by Railway (see /Procfile).
# Builds the vector store on first boot, then launches the API.
set -e

cd "$(dirname "$0")"          # -> the backend/ folder
export PYTHONPATH="$PWD"      # so `import app` works without an editable install

# Build the Chroma store the first time (persisted if a volume is mounted).
if [ ! -f "chroma_db/chroma.sqlite3" ]; then
  echo "No vector store found - running ingestion (one-time)..."
  python scripts/ingest.py
fi

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
