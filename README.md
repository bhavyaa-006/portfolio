# Modern Full-Stack Portfolio

A production-ready, modern portfolio website built with React, Vite, Tailwind CSS, Framer Motion, and FastAPI.

## Architecture
- **Frontend:** React + Vite + Tailwind CSS + Framer Motion
- **Backend:** FastAPI + SQLAlchemy + SQLite (Development) / PostgreSQL (Production)
- **State Management:** Zustand
- **API Communication:** Axios

## Getting Started Locally

### Using Docker (Recommended)
You can run the entire stack using Docker Compose:
```bash
docker-compose up --build
```
- Frontend will be available at `http://localhost:5173`
- Backend API will be available at `http://localhost:8000`
- Swagger Docs will be available at `http://localhost:8000/docs`

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
2. Set the Framework Preset to Vite.
3. Add Environment Variable: `VITE_API_URL` pointing to your backend URL.

### Backend (Render / Railway)
1. Connect your repository to Render or Railway.
2. Select the `/backend` directory.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Add Environment Variables:
   - `DATABASE_URL` (Neon Postgres Connection String)
   - `SECRET_KEY` (Generate a secure random string)
   - `BACKEND_CORS_ORIGINS` (Your Vercel frontend URL, e.g. `["https://your-portfolio.vercel.app"]`)

### Database (Neon)
1. Create a Neon Postgres database.
2. Get the connection string (e.g. `postgresql+asyncpg://user:pass@ep-cool.neon.tech/dbname`).
3. Set this string as `DATABASE_URL` in your backend environment.

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
