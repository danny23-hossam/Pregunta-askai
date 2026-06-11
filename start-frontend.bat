@echo off
REM Starts the Pregunta frontend (React + Vite) without Docker.
REM Requires: Node.js 18+.

cd /d "%~dp0frontend\my-app"

echo Installing frontend dependencies (first run may take a minute)...
call npm install

echo Starting frontend on http://localhost:5173 ...
call npm run dev -- --host 0.0.0.0 --port 5173

pause
