import logging
import os
import subprocess
import sys
import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.db.session import engine

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("portfolio.startup")


def validate_application_import() -> None:
    logger.info("Preflight check: importing FastAPI application")
    try:
        import app.main  # noqa: F401
    except ImportError as exc:
        message = str(exc)
        if "email-validator" in message or "email_validator" in message:
            logger.exception(
                "Missing dependency detected while importing the application"
            )
            raise RuntimeError(
                "Backend startup failed because the email validation dependency is missing. "
                "Rebuild the Docker image after installing requirements."
            ) from exc

        logger.exception("Application import failed during startup preflight")
        raise


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


def main() -> None:
    validate_application_import()

    logger.info("Waiting for PostgreSQL to become ready")
    wait_for_database()
    if settings.RUN_MIGRATIONS:
        logger.info("Applying Alembic migrations")
        run_migrations()
    else:
        logger.info("Skipping Alembic migrations (RUN_MIGRATIONS=false)")

    uvicorn_args = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        os.getenv("PORT", "8000"),
        "--proxy-headers",
        "--log-level",
        settings.LOG_LEVEL.lower(),
    ]

    if os.getenv("UVICORN_RELOAD", "false").lower() in {"1", "true", "yes"}:
        uvicorn_args.append("--reload")

    logger.info("Starting API server")
    os.execvp(uvicorn_args[0], uvicorn_args)


if __name__ == "__main__":
    main()