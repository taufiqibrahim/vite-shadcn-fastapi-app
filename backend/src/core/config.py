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

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    DEMO_USER_EMAIL: EmailStr
    DEMO_USER_PASSWORD: str

    # UploadThing
    UPLOADTHING_SECRET: str = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "fastapi-backend"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]

    JWT_ENCODE_ALGORITHM: str = "HS256"

    UPLOAD_BACKEND: Literal["s3", "uploadthing"] = "uploadthing"
    UPLOAD_BACKEND_S3_BUCKET_NAME: str = None


settings = Settings()
secret_settings = SecretSettings()
