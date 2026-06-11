#!/usr/bin/env bash
# Starts the Pregunta frontend (React + Vite) without Docker.
# Requires: Node.js 18+.
set -e

cd "$(dirname "$0")/frontend/my-app"

echo "Installing frontend dependencies (first run may take a minute)..."
npm install

echo "Starting frontend on http://localhost:5173 ..."
npm run dev -- --host 0.0.0.0 --port 5173
