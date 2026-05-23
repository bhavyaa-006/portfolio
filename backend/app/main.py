from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.session import SessionLocal
from app.middleware.error_handlers import register_error_handlers
from app.routes.auth import router as auth_router
from app.routes.health import router as health_router
from app.routes.portfolio import admin_router, router as portfolio_router
from app.services.auth_service import bootstrap_admin_user

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger(__name__)


def run_migrations() -> None:
    alembic_config = Config(str(BASE_DIR / "alembic.ini"))
    command.upgrade(alembic_config, "head")


def bootstrap_admin() -> None:
    with SessionLocal() as session:
        bootstrap_admin_user(session)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logger.info("Starting %s on %s", settings.PROJECT_NAME, settings.API_V1_STR)

    if settings.RUN_MIGRATIONS:
        last_error: Exception | None = None
        for attempt in range(5):
            try:
                run_migrations()
                logger.info("Database migrations completed")
                last_error = None
                break
            except Exception as exc:  # pragma: no cover - startup retry path
                last_error = exc
                if attempt == 4:
                    raise
                time.sleep(2)
        if last_error is not None:
            raise last_error

    bootstrap_admin()
    yield


app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", lifespan=lifespan)
register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(health_router)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(portfolio_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
