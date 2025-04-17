import asyncio
import uuid
from fastapi import UploadFile
from sqlmodel import Session, select
from src.apps.models import App
from src.apps.schemas import AppCreate
from src.apps.services import create_app
from src.auth.models import UserProfile
from src.core.config import secret_settings
from src.database.session import engine
from src.core.logging import get_logger, setup_logging
from src.geospatial_mapping.services import create_dataset

setup_logging()
logger = get_logger(__name__)
from src.files.services import handle_upload_minio
from src.geospatial_mapping.models import Dataset, StorageBackend
from src.geospatial_mapping.schemas import DatasetCreate
from src.users.schemas import AccountCreate, UserProfileCreate
from src.users.services import create_user_account, create_user_profile, get_account_by_email


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
            created_account = create_user_account(db=session, account=u)
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


async def load_geospatial_mapping_data(session: Session) -> None:
    demo_account = get_account_by_email(db=session, email=secret_settings.DEMO_USER_EMAIL)
    datasets = [
        DatasetCreate(
            uid=uuid.uuid4(),
            account_id=demo_account.id,
            name="open_energy_sample",
            description="open_energy_sample",
            file_name="open_energy_sample.json",
            storage_backend="minio",
            storage_uri="",
            status="uploaded",
        ),
    ]

    for d in datasets:
        logger.info(f"Creating dataset {d.name} using demo data data/{d.file_name}")

        # upload to minio
        file_path = f"src/scripts/data/{d.file_name}"
        with open(file_path, "rb") as f:
            upload_file = UploadFile(filename=d.file_name, file=f)
            upload_response = await handle_upload_minio(file=upload_file, account_uid=demo_account.uid)
            print(upload_response)

        db_dataset = session.exec(
            select(Dataset).where(Dataset.account_id == demo_account.id, Dataset.name == d.name)
        ).first()
        if db_dataset:
            logger.info("Dataset already registered")
        else:
            d.storage_uri = upload_response["storage_uri"]
            created_dataset = create_dataset(db=session, dataset=d)
            logger.info(f"Dataset created: {created_dataset.name}")


def init() -> None:
    with Session(engine) as session:
        load_data(session)
        asyncio.run(load_geospatial_mapping_data(session))


if __name__ == "__main__":
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data created")
