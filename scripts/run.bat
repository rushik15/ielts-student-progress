@echo off
setlocal
where python >nul 2>nul || (echo Python is required. Install Python 3.11+ and retry.& exit /b 1)
where npm >nul 2>nul || (echo Node.js/npm is required. Install Node 20+ and retry.& exit /b 1)
cd /d %~dp0..
if not exist backend\.venv python -m venv backend\.venv
call backend\.venv\Scripts\activate.bat
pip install -r backend\requirements.txt
if not exist backend\.env copy backend\.env.example backend\.env >nul
if not exist frontend\node_modules call npm --prefix frontend install
start "IELTS API" cmd /k "cd /d %CD%\backend && .venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8001"
start "IELTS Frontend" cmd /k "cd /d %CD%\frontend && npm run dev"
echo Frontend: http://localhost:5173  API: http://127.0.0.1:8001/docs
