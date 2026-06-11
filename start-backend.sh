#!/usr/bin/env bash
# Starts the Pregunta backend (FastAPI) without Docker.
# Requires: Python 3.11+, MySQL running, MongoDB running.
set -e

cd "$(dirname "$0")/backend"

if [ ! -d venv ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Installing backend dependencies..."
pip install --disable-pip-version-check -r requirements.txt

echo "Starting backend on http://localhost:8000 ..."
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
