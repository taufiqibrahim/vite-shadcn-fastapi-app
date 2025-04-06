import logging

from sqlmodel import Session, select
from apps.users.models import User, UserCreate
from apps.users import user_crud
from core.config import settings
from core.database import engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(session: Session) -> None:
    # superuser = session.exec(
    #     select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    # ).first()
    # if not superuser:
    #     superuser_create = UserCreate(
    #         email=settings.FIRST_SUPERUSER_EMAIL,
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         is_superuser=True,
    #     )
    #     print(superuser_create)
    #     # user = crud.create_user(session=session, user_create=user_create)

    demouser = session.exec(
        select(User).where(User.email == settings.DEMO_USER_EMAIL)
    ).first()
    if not demouser:
        demouser_create = UserCreate(
            email=settings.DEMO_USER_EMAIL,
            password=settings.DEMO_USER_PASSWORD,
            is_superuser=True,
        )
        print(demouser_create)
        user = user_crud.create_user(session=session, user_create=demouser_create)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


if __name__ == "__main__":
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data created")
