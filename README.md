# Modern Full-Stack Portfolio

Monorepo for a React/Vite frontend and a clean FastAPI backend deployed on Render with Neon PostgreSQL.

## Architecture
- Frontend: React + Vite + Tailwind CSS + Zustand + Axios
- Backend: FastAPI + SQLAlchemy + Alembic + JWT auth
- Database: Neon PostgreSQL
- Deployments: Render backend, Vercel frontend

## Local development
Backend:
1. `cd backend`
2. Create a Python 3.14 virtual environment.
3. `pip install -r requirements.txt`
4. Copy `backend/.env.example` to `backend/.env` and set `DATABASE_URL`
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload`

Frontend:
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Deployment
Render backend:
- Root Directory: `backend`
- Build Command: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
- Start Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Runtime: `python-3.14.0`

Vercel frontend:
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`

## Frontend API URL
Set `VITE_API_URL` to the backend origin, for example `https://your-backend.onrender.com`. The frontend client appends `/api/v1` automatically.
