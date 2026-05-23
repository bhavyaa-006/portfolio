import logging
import os
import subprocess
import sys
import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.db.session import engine

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("portfolio.startup")


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
    wait_for_database()
    run_migrations()

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
    ]

    if os.getenv("UVICORN_RELOAD", "false").lower() in {"1", "true", "yes"}:
        uvicorn_args.append("--reload")

    logger.info("Starting API server")
    os.execvp(uvicorn_args[0], uvicorn_args)


if __name__ == "__main__":
    main()