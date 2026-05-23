from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.core.config import settings
from app.database.session import SessionLocal, engine
from app.middleware.error_handlers import register_error_handlers
from app.routes.auth import router as auth_router
from app.routes.health import router as health_router
from app.routes.portfolio import admin_router, router as portfolio_router
from app.services.auth_service import bootstrap_admin_user

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger(__name__)


def _redacted_database_url() -> str:
    try:
        return make_url(settings.DATABASE_URL).render_as_string(hide_password=True)
    except Exception:
        return "<invalid database url>"


def _configure_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,
    )


def _check_database_connection() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def run_migrations() -> None:
    alembic_config = Config(str(BASE_DIR / "alembic.ini"))
    command.upgrade(alembic_config, "head")


def bootstrap_admin() -> None:
    with SessionLocal() as session:
        bootstrap_admin_user(session)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Application startup beginning")
    logger.info("Project: %s", settings.PROJECT_NAME)
    logger.info("API prefix: %s", settings.API_V1_STR)
    logger.info("Database URL: %s", _redacted_database_url())
    logger.info("Migrations enabled: %s", settings.RUN_MIGRATIONS)

    if settings.RUN_MIGRATIONS:
        for attempt in range(5):
            try:
                _check_database_connection()
                await asyncio.to_thread(run_migrations)
                logger.info("Database migrations completed")
                break
            except Exception:
                logger.exception("Startup migration attempt %s of 5 failed", attempt + 1)
                if attempt == 4:
                    logger.warning("Continuing startup without completed migrations")
                    break
                await asyncio.sleep(2)

    try:
        await asyncio.to_thread(bootstrap_admin)
        logger.info("Admin bootstrap check completed")
    except Exception:
        logger.exception("Admin bootstrap failed during startup")

    logger.info("Application startup finished")
    yield
    logger.info("Application shutdown beginning")


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


def run() -> None:
    _configure_logging()
    port = int(os.environ.get("PORT", 8000))
    logger.info("Starting server on 0.0.0.0:%s", port)
    logger.info("Render health check path: /health")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port, log_level=settings.LOG_LEVEL.lower())


if __name__ == "__main__":
    run()
