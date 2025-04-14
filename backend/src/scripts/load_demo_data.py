import logging

from sqlmodel import Session, select
from src.apps.models import App
from src.apps.schemas import AppCreate
from src.apps.services import create_app
from src.auth.models import UserProfile
from src.core.config import settings, secret_settings
from src.database.session import engine
from src.core.logging import logger
from src.users.schemas import AccountCreate, UserProfileCreate
from src.users.services import create_account, create_user_profile, get_account_by_email


def load_data(session: Session) -> None:

    users = [
        AccountCreate(
            email=secret_settings.FIRST_SUPERUSER_EMAIL,
            password=secret_settings.FIRST_SUPERUSER_PASSWORD,
            full_name=secret_settings.FIRST_SUPERUSER_EMAIL,
        ),
        AccountCreate(
            email=secret_settings.DEMO_USER_EMAIL,
            password=secret_settings.DEMO_USER_PASSWORD,
            full_name=secret_settings.DEMO_USER_EMAIL,
        ),
    ]

    for u in users:
        logger.info(f"Creating user: {u.email}")
        db_account = get_account_by_email(db=session, email=u.email)
        if db_account:
            logger.info("Email already registered")
        else:
            created_account = create_account(db=session, account=u)
            profile_create = UserProfileCreate(account_id=created_account.id, full_name=u.full_name)
            create_user_profile(db=session, account_id=created_account.id, profile=profile_create)
            user_profile = session.exec(select(UserProfile).where(UserProfile.id == created_account.id)).first()
            logger.info(f"User created: {user_profile}")

    apps = [
        AppCreate(
            name="geospatial-mapping-app",
            description="A modular platform that enables users to upload geospatial datasets, configure and run cloud-hosted spatial algorithms, and interactively visualize the results on a map",
        ),
    ]

    for a in apps:
        logger.info(f"Creating app: {a.name}")
        db_app = session.exec(select(App).where(App.name == a.name)).first()

        if not db_app:
            db_app = create_app(db=session, app=a)
            logger.info(f"App created: {db_app}")


def init() -> None:
    with Session(engine) as session:
        load_data(session)


if __name__ == "__main__":
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data created")
