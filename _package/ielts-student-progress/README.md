# IELTS Student Progress Portal

A full-stack portal for recording IELTS Listening, Reading, and Writing practice. Students can enter their own test results and mistakes, while teachers/admins can create students, inspect progress, and manage records.

## Project layout

```text
backend/     FastAPI API, SQLAlchemy models, tests, Dockerfile
frontend/    React + Vite + TypeScript single-page application
scripts/     Windows starter and stopper scripts
SRS.md       Product requirements
```

## Quick start on Windows

Install Python 3.11+ and Node.js 20+, then double-click `scripts/run.bat` (or run `./scripts/run.ps1` in PowerShell). It creates the virtual environment, installs packages, creates the development backend `.env`, and opens separate API/frontend terminals.

Open `http://localhost:5173`. The initial development admin is `admin001` / `change-me-now`; change it immediately after first use. API documentation is at `http://127.0.0.1:8000/docs`. Run `scripts/stop.bat` to stop development servers.

Manual setup:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

cd ..\frontend
npm install
copy .env.example .env
npm run dev
```

On macOS/Linux use `python3 -m venv backend/.venv`, `source backend/.venv/bin/activate`, then the same pip/npm/uvicorn commands (with forward slashes).

## Using the portal

An admin or teacher creates students from **Students**. Students then sign in with their student number and temporary password, add results (including repeatable mistake rows), inspect charts and history, and change their password. Teachers can search/open a student, add/edit/delete results, inspect all three charts, and reset a student password. Admins can create teacher accounts through the API by posting a `role: "teacher"` payload to `POST /api/v1/students`.

## Environment variables

Backend (`backend/.env`):

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Long random JWT signing secret; required to be changed in production. |
| `DATABASE_URL` | Local `sqlite:///./ielts_progress.db` or production `postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime, default 1440. |
| `CORS_ORIGINS` | Comma-separated frontend origins, e.g. `https://portal.example.com`. |
| `BOOTSTRAP_ADMIN_NUMBER`, `BOOTSTRAP_ADMIN_PASSWORD`, `BOOTSTRAP_ADMIN_NAME` | First-run admin account only. Change from examples before deployment. |

Frontend (`frontend/.env`): `VITE_API_BASE_URL`, e.g. `https://your-api.onrender.com/api/v1`. It is intentionally not hard-coded for production.

## Tests and builds

```powershell
backend\.venv\Scripts\python -m compileall backend\app
backend\.venv\Scripts\python -m pytest backend\tests -q
npm --prefix frontend run build
```

## Deployment

1. Create a managed PostgreSQL database and set its `DATABASE_URL` on the backend service.
2. Deploy `backend/` as the Docker service defined by `render.yaml`; configure `SECRET_KEY`, `CORS_ORIGINS`, bootstrap values, and `DATABASE_URL`. Render supplies `PORT` automatically. The API creates missing tables safely at startup; it never drops data.
3. Deploy `frontend/` to Vercel or Netlify. Set `VITE_API_BASE_URL` to the deployed backend URL plus `/api/v1`. `vercel.json` and `netlify.toml` provide SPA refresh fallbacks.
4. Set backend `CORS_ORIGINS` to the exact deployed frontend URL, then test `/api/v1/health`, admin login, and a student score entry.

For local container PostgreSQL, run `docker compose up --build` and serve the frontend separately with `npm --prefix frontend run dev` using a matching frontend API URL.

## Common problems

- **CORS or network error:** ensure `VITE_API_BASE_URL` is correct and `CORS_ORIGINS` includes the frontend origin exactly.
- **Login fails:** verify the bootstrap password in the backend environment and restart after changing it only before first startup.
- **Database connection error:** use a SQLAlchemy URL beginning with `postgresql+psycopg://` for PostgreSQL and ensure the database is reachable.
- **Port in use:** use `scripts/stop.bat` or change the Uvicorn/Vite port.
