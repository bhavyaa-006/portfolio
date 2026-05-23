import json
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Portfolio API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="supersecretkey-change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./portfolio.db")
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_RECYCLE: int = Field(default=300)

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:4173",
        ]
    )
    BACKEND_CORS_ORIGIN_REGEX: str = Field(default=r"^https://.*\.vercel\.app$")

    LOG_LEVEL: str = Field(default="INFO")
    RUN_MIGRATIONS: bool = Field(default=True)

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if not isinstance(value, str):
            return value

        normalized = value.strip()
        if normalized.startswith("postgres://"):
            normalized = normalized.replace("postgres://", "postgresql://", 1)

        parsed = urlsplit(normalized)
        hostname = parsed.hostname or ""
        if hostname.endswith("neon.tech"):
            query = dict(parse_qsl(parsed.query, keep_blank_values=True))
            query.setdefault("sslmode", "require")
            normalized = urlunsplit(
                (parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment)
            )

        if normalized.startswith("sqlite:///") or normalized.startswith("sqlite+pysqlite:///"):
            return normalized
        if normalized.startswith("postgresql+psycopg://"):
            return normalized
        if normalized.startswith("postgresql+psycopg2://"):
            return normalized.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)
        if normalized.startswith("postgresql://"):
            return normalized.replace("postgresql://", "postgresql+psycopg://", 1)
        if normalized.startswith("postgres://"):
            return normalized.replace("postgres://", "postgresql+psycopg://", 1)
        return normalized

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_backend_cors_origins(cls, value):
        if value in (None, ""):
            return ["http://localhost:5173", "http://127.0.0.1:5173"]
        if isinstance(value, str):
            text = value.strip()
            if text.startswith("["):
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in text.split(",") if origin.strip()]
        return value

settings = Settings()
