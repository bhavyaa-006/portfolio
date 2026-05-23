# Portfolio Backend

Clean FastAPI backend for the portfolio monorepo.

## Stack
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL on Neon
- JWT authentication
- Pydantic

## Local setup
1. `cd backend`
2. Create a Python 3.14 virtual environment.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set `DATABASE_URL`.
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload`

## Render deployment
- Root Directory: `backend`
- Build Command: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Runtime: `python-3.14.0`

## API contract with the frontend
- Public reads are under `/api/v1/portfolio/*`
- Login uses `POST /api/v1/auth/login/access-token` with form-urlencoded `username` and `password`
- Login returns `access_token` at the top level
- Frontend API base URL should point to the backend origin, and the client appends `/api/v1`
