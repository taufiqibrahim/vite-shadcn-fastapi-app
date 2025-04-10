import logging

from sqlmodel import Session, select
from backend.users.models import User, UserCreate
from backend.users import user_crud
from backend.apps.models import App, AppCreate
from backend.apps import apps_crud
from backend.core.config import settings
from backend.core.database import engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db_users(session: Session) -> None:
    pass


def init_db(session: Session) -> None:

    users = [
        UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        ),
        UserCreate(
            email=settings.DEMO_USER_EMAIL,
            password=settings.DEMO_USER_PASSWORD,
            is_superuser=True,
        ),
    ]

    for u in users:
        logger.info(f"Creating user: {u.email}")
        user = session.exec(select(User).where(User.email == u.email)).first()
        if not user:
            user = user_crud.create_user(session=session, user_create=u)

    apps = [
        AppCreate(
            name="geospatial-mapping-app",
            description="A modular platform that enables users to upload geospatial datasets, configure and run cloud-hosted spatial algorithms, and interactively visualize the results on a map",
        ),
    ]

    for a in apps:
        logger.info(f"Creating app: {a.name}")
        _app = session.exec(select(App).where(App.name == a.name)).first()

        if not _app:
            _app = apps_crud.create_app(session=session, app_create=a)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


if __name__ == "__main__":
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data created")
