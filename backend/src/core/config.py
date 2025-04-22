import secrets
from typing import Annotated, Any, Literal
from pydantic import AnyUrl, BeforeValidator, EmailStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class SecretSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///db.sqlite3"
    UPLOAD_BACKEND_UPLOADTHING_SECRET: str = "sk_live_****"


class DemoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changeme"
    DEMO_USER_EMAIL: EmailStr = "demo@example.com"
    DEMO_USER_PASSWORD: str = "changeme"
    DEMO_SERVICE_ACCOUNT_EMAIL: EmailStr = "demo-sa@example.com"
    DEMO_SERVICE_ACCOUNT_APIKEY: str = "changeme"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    LOG_LEVEL: str = "warning"
    PROJECT_NAME: str = "fastapi-backend"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]

    ALGORITHM: str = "HS256"
    ENABLE_SERVICE_ACCOUNT_AUTH: bool = True
    API_KEY_HEADER: str = "x-api-key"

    UPLOAD_BACKEND: Literal["minio", "s3", "uploadthing"] = "minio"
    UPLOAD_BACKEND_S3_BUCKET_NAME: str = "your-s3-bucket-name"

    WORKFLOW_BACKEND: Literal["temporal"] = "temporal"
    TEMPORAL_ADDRESS: str = "localhost:7233"


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "changeme123"
    MINIO_SECURE: bool = False


class PostgisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    POSTGIS_HOST: str = "127.0.0.1"
    POSTGIS_DB: str = "app"
    POSTGIS_USER: str = "app"
    POSTGIS_PASSWORD: str = "changeme123"
    POSTGIS_PORT: str = "5432"


settings = Settings()
demo_settings = DemoSettings()
secret_settings = SecretSettings()
minio_settings = MinioSettings()
postgis_settings = PostgisSettings()
