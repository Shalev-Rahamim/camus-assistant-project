## Campus Elad Software – AI Campus Assistant

### Overview
Smart Campus Assistant is an AI-powered platform developed during a hackathon in collaboration with Elad Software. It utilizes a RAG architecture (FastAPI, SQLite, Google Gemini) to provide students with instant, reliable answers about campus schedules, facilities, and policie

- **Backend**: FastAPI, async SQLAlchemy, SQLite (dev), Gemini (google‑genai)
- **Frontend**: Vanilla JS, HTML, CSS (hash‑based routing, single‑page feel)
- **AI**: Classification + RAG pipeline + Gemini LLM

### Project Structure (High‑Level)

- `backend/`
  - `main.py` – FastAPI app entrypoint, CORS, routers registration
  - `api/` – HTTP API:
    - `routes.py` – public endpoints (`/`, `/ask`)
    - `tables.py` – read‑only tables (schedules, knowledge base)
    - `conversations.py` – chat history & conversations
    - `admin/` – admin login & dashboard (JWT)
  - `ai/` – AI logic:
    - `rag.py` – RAG orchestration
    - `classifier.py` – question classification
    - `llm_client.py` – Gemini client
    - `prompt_manager.py` – system prompts & prompt builder
  - `db/` – database layer:
    - `models.py` – SQLAlchemy models
    - `database.py` – engine, sessions, init_db
    - `repository.py` – DB queries, logs
    - `seed.py` – seed demo data
    - `create_admin.py` – create admin user
  - `core/` – cross‑cutting utilities (security, rate limiting)
  - `tests/` – backend tests

- `frontend/`
  - `index.html` – single HTML shell
  - `app.js` – main UI logic & rendering
  - `api.js` – frontend API client
  - `router.js` – simple client router (hash‑based)
  - `styles.css` – layout & design
  - `static/` – images (logos)

### Prerequisites

- Python **3.11+**
- Node.js **(optional, only if you prefer a static file server – otherwise any simple HTTP server is fine)**

---

### 1. Backend Setup

```bash
cd backend

# (optional but recommended) create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # on Windows
# source .venv/bin/activate  # on macOS / Linux

# install dependencies
pip install -r requirements.txt
```

#### Environment Variables

In the **project root** (same level as `backend/` and `frontend/`), copy the template and fill in your secrets:

```bash
cp .env.example .env
```

Required variables (see `.env.example`):

- `GEMINI_API_KEY` – Google Gemini API key
- `SECRET_KEY` – secret key for admin JWT tokens
- `DATABASE_URL` – (optional) SQLAlchemy URL. Defaults to SQLite file if not set:
  - `sqlite+aiosqlite:///./campus_assistant.db`

#### Initialize Database (First Time)

```bash
cd backend

# Create tables and run lightweight migrations
python -m db.seed

# (optional) create admin user
python -m db.create_admin admin your_strong_password
```

#### Run the Backend Server

From the `backend/` folder:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000/api/v1`

---

### 2. Frontend Setup

No build tools are required – the frontend is plain HTML/JS/CSS.

From the project root:

```bash
cd frontend

# Option A: Python simple HTTP server
python -m http.server 5500

# Open in browser:
# http://localhost:5500/index.html
```

The frontend expects the backend at `http://localhost:8000/api/v1` (configured in `frontend/api.js`).

---

### 3. Environment Variables (.env)

The backend loads environment variables using `python-dotenv` (`load_dotenv()` in `backend/ai/llm_client.py` and `backend/api/admin/auth.py`), and `DATABASE_URL` is read in `backend/db/database.py`.

Use the `.env.example` file in the **project root** as a template. Rename / copy it to `.env` and fill in real values.

---

### 4. Running Tests (Backend)

From `backend/`:

```bash
pytest
```

This will run unit and integration tests for the RAG pipeline, security, and database logic.

---

- My tests: 127 from 127 passed


### 5. Deployment Notes (Basic)

- For development: SQLite + `uvicorn --reload` is enough.
- For staging/production:
  - Switch `DATABASE_URL` to a managed Postgres instance.
  - Set strong `SECRET_KEY` and `GEMINI_API_KEY` in the server environment.
  - Put FastAPI behind a reverse proxy (e.g., Nginx) and serve `frontend/` as static files.

