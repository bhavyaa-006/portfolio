import logging
import os
import sys

from app.core.config import settings

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("portfolio.startup")

def main() -> None:
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