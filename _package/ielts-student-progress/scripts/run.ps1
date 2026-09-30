$ErrorActionPreference = 'Stop'; $root = Split-Path $PSScriptRoot -Parent
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3.11+ is required.' }
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) { throw 'Node.js/npm is required.' }
Set-Location $root
if (-not (Test-Path backend/.venv)) { python -m venv backend/.venv }
& backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
if (-not (Test-Path backend/.env)) { Copy-Item backend/.env.example backend/.env }
if (-not (Test-Path frontend/node_modules)) { npm.cmd --prefix frontend install }
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root/backend'; .venv/Scripts/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root/frontend'; npm.cmd run dev"
Write-Host 'Frontend: http://localhost:5173  API docs: http://127.0.0.1:8000/docs'
