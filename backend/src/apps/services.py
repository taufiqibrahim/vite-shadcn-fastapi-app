import uuid
from sqlmodel import Session, select
from src.apps.models import App
from src.apps.schemas import AppCreate, AppRead
from src.core.logging import get_logger

logger = get_logger(__name__)


def create_app(db: Session, app: AppCreate):
    logger.debug(f"create_app {app}")
    db_app = App(
        name=app.name,
        description=app.description,
        uid=uuid.uuid4(),
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def get_apps(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(App).offset(skip).limit(limit)).all()
