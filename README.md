# Modern Full-Stack Portfolio

A production-ready, modern portfolio website built with React, Vite, Tailwind CSS, Framer Motion, and FastAPI.

## Architecture
- **Frontend:** React + Vite + Tailwind CSS + Framer Motion
- **Backend:** FastAPI + SQLAlchemy + SQLite (Development) / PostgreSQL (Production)
- **State Management:** Zustand
- **API Communication:** Axios

## Getting Started Locally

### Manual Setup
#### Backend
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate` (or `.\venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload`

#### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Deployment

### Frontend (Vercel)
1. Import the `/frontend` directory to Vercel.
2. Set the Root Directory to `frontend`.
3. Keep the Framework Preset set to Vite.
4. Add `VITE_API_URL` with your Render backend base URL, for example `https://your-backend.onrender.com`.
5. Keep `frontend/vercel.json` so React Router deep links rewrite to `index.html`.

### Backend (Render)
1. Deploy from the repo root using `render.yaml`.
2. Set the Root Directory to `backend`.
3. Use the Python runtime with build command `pip install -r requirements.txt`.
4. Use start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
5. Add environment variables:
  - `DATABASE_URL` for your Neon PostgreSQL connection string.
  - `SECRET_KEY` as a strong random value.
  - `BACKEND_CORS_ORIGINS` including your Vercel domain, for example `["https://your-frontend.vercel.app"]`.
  - `BACKEND_CORS_ORIGIN_REGEX` if you want to allow all `vercel.app` previews.
  - `RUN_MIGRATIONS=true`.

### Database (Neon)
1. Create a Neon Postgres database.
2. Copy the pooled or direct PostgreSQL connection string.
3. Set it as `DATABASE_URL` in Render.
4. Keep `sslmode=require` enabled; the backend normalizes Neon URLs automatically.

## Initial Admin Setup
To create your first admin user, send a POST request to `/api/v1/setup`:
```json
{
  "email": "admin@example.com",
  "password": "securepassword",
  "name": "Admin Name"
}
```
*Note: In production, ensure this endpoint is disabled or protected after initial setup.*
