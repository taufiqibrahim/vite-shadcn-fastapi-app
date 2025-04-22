from sqlmodel import create_engine, Session, SQLModel
from src.core.config import secret_settings


if secret_settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    engine = create_engine(secret_settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
else:
    engine = create_engine(secret_settings.SQLALCHEMY_DATABASE_URI)


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    engine = create_engine(secret_settings.SQLALCHEMY_DATABASE_URI)
    SQLModel.metadata.create_all(engine)
