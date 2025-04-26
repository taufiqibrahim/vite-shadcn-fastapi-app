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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    LOG_LEVEL: str = "warning"
    PROJECT_NAME: str = "fastapi-backend"
    BRAND_NAME: str = "tibrahim.dev"
    APP_URL: str = "https://www.example.com"
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "staging"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1  # default 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # default 7 days
    RESET_TOKEN_EXPIRY_MINUTES: int = 15  # default 15 minutes
    ENABLE_SERVICE_ACCOUNT_AUTH: bool = True
    API_KEY_HEADER: str = "x-api-key"

    UPLOAD_BACKEND: Literal["minio", "s3", "uploadthing"] = "minio"
    UPLOAD_BACKEND_S3_BUCKET_NAME: str = "your-s3-bucket-name"

    WORKFLOW_BACKEND: Literal["temporal"] = "temporal"
    TEMPORAL_ADDRESS: str = "localhost:7233"


class SecretSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///db.sqlite3"
    UPLOAD_BACKEND_UPLOADTHING_SECRET: str = "sk_live_****"


class MailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    MAIL_ENABLED: bool = True
    MAIL_SMTP_HOST: str = "smtp.zoho.com"
    MAIL_SMTP_PORT: int = 587
    MAIL_SMTP_USERNAME: str = "your-email@yourdomain.com"
    MAIL_SMTP_PASSWORD: str = "your-app-password"


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
mail_settings = MailSettings()
