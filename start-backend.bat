@echo off
REM Starts the Pregunta backend (FastAPI) without Docker.
REM Requires: Python 3.11+, XAMPP MySQL running, MongoDB running.

cd /d "%~dp0backend"

if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing backend dependencies...
pip install --disable-pip-version-check -r requirements.txt

echo Starting backend on http://localhost:8000 ...
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

pause
