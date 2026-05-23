import logging
import subprocess
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.db.session import engine

# Create tables for dev (Alembic should be used in prod)
# Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def wait_for_database(timeout_seconds: int = 90, interval_seconds: int = 2) -> None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection established")
            return
        except OperationalError as exc:
            if time.monotonic() >= deadline:
                logger.exception("Database did not become ready in time")
                raise
            logger.info("Waiting for database: %s", exc)
            time.sleep(interval_seconds)


def run_migrations() -> None:
    logger.info("Running Alembic migrations")
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logger.info("Backend startup initiated")
    wait_for_database()
    if settings.RUN_MIGRATIONS:
        run_migrations()
    else:
        logger.info("Skipping Alembic migrations (RUN_MIGRATIONS=false)")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

from app.api.api import api_router

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

from fastapi.staticfiles import StaticFiles

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

@app.get("/")
def root():
    return {"message": "Welcome to the Portfolio API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
