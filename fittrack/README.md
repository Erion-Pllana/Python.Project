# FitTrack

FitTrack is a Fitness Center / Gym Management System.

**Stack:** Streamlit (frontend) → FastAPI (backend) → SQLAlchemy → MySQL,
with Pandas + Plotly for analytics. Python only — no HTML/CSS/JS
frontend, no PHP, no other web frameworks.

```
Streamlit  →  FastAPI  →  Python business logic  →  SQLAlchemy  →  MySQL
```

## Status: Step 1 — Project Initialization

This step only sets up the skeleton and confirms both servers start and
can talk to each other. No auth, no database tables, no features yet.

## Project structure

```
fittrack/
├── backend/
│   ├── main.py            FastAPI app entrypoint
│   ├── config.py          Centralized settings (reads .env)
│   ├── database/
│   │   └── session.py     SQLAlchemy engine/session setup (not queried yet)
│   ├── models/             (empty — SQLAlchemy ORM models, Step 3+)
│   ├── schemas/             (empty — Pydantic request/response schemas)
│   ├── routers/
│   │   └── health.py      GET /api/health
│   ├── services/            (empty — business logic, later steps)
│   └── security/            (empty — auth/JWT logic, Step 2+)
│
├── frontend/
│   ├── app.py              Streamlit entrypoint
│   ├── api_client.py       HTTP client that calls the FastAPI backend
│   ├── config.py           Reads API_BASE_URL from .env
│   ├── auth.py              (placeholder — login/session, Step 2+)
│   ├── state.py             (placeholder — shared session state)
│   ├── pages/                (empty — multi-page app screens, later steps)
│   └── components/           (empty — reusable UI pieces, later steps)
│
├── database/
│   ├── schema.sql          MySQL schema (empty placeholder — Step 3+)
│   └── seed.sql            Sample data (empty placeholder — Step 3+)
│
├── tests/
│   └── test_health.py      Confirms FastAPI boots and /api/health works
│
├── .env.example             Copy to .env and fill in values
├── requirements.txt
└── README.md
```

## What each new file does

| File | Purpose |
|---|---|
| `backend/main.py` | Creates the FastAPI app, adds CORS (so Streamlit can call it), registers routers, defines `GET /` |
| `backend/config.py` | Loads all configuration (ports, URLs, DB credentials, secret key) from `.env` via `pydantic-settings` into one `settings` object |
| `backend/routers/health.py` | Defines `GET /api/health` → `{"status": "ok", "application": "FitTrack"}` |
| `backend/database/session.py` | Sets up the SQLAlchemy engine, `SessionLocal`, and declarative `Base` for MySQL. Wired now so later steps just add models — nothing queries the DB yet |
| `frontend/app.py` | The Streamlit page: shows the "FITTRACK / Fitness Management System" header and calls the backend's health endpoint to show Connected / Not Connected |
| `frontend/api_client.py` | The **only** place the frontend talks to the backend, via `httpx`. Streamlit never touches MySQL directly |
| `frontend/config.py` | Reads `API_BASE_URL` from `.env` for the frontend process |
| `frontend/auth.py`, `frontend/state.py` | Empty placeholders for Step 2+ (login, session state) |
| `database/schema.sql`, `database/seed.sql` | Empty placeholders for Step 3+ |
| `tests/test_health.py` | `pytest` smoke test hitting `/api/health` and `/` |
| `.env.example` | Template for all environment variables (app, backend, frontend, MySQL, JWT secret) |
| `requirements.txt` | All pinned dependencies for both backend and frontend |

## 1. Install dependencies

From the `fittrack/` project root:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
```

The defaults in `.env.example` are enough to run Step 1 (FastAPI +
Streamlit + health check). The `DB_*` and `SECRET_KEY` values aren't
used yet — they're there so the config layer is already complete for
later steps.

## 3. Start FastAPI (backend)

From the `fittrack/` project root (important — so the `backend` package
resolves correctly):

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

## 4. Start Streamlit (frontend)

In a **second terminal**, also from the `fittrack/` project root:

```bash
streamlit run frontend/app.py
```

This opens a browser tab (usually `http://localhost:8501`).

## 5. Verify everything works

- **FastAPI directly:** open `http://127.0.0.1:8000/api/health` in a
  browser — you should see:
  ```json
  {"status": "ok", "application": "FitTrack"}
  ```
  You can also check interactive docs at `http://127.0.0.1:8000/docs`.

- **Streamlit:** the page should show:
  ```
  FITTRACK
  Fitness Management System
  Backend Status: Connected · FitTrack
  ```
  If FastAPI isn't running, it will show **Backend Status: Not
  Connected** instead — start the backend and click "Re-check backend
  connection".

- **Automated check:**
  ```bash
  pytest
  ```
  Both tests in `tests/test_health.py` should pass.

## Not implemented yet (by design)

Authentication, database tables, CRUD, member management, workouts,
classes, and analytics dashboards are intentionally **not** part of
Step 1. These arrive in later steps once this foundation is confirmed
working.
