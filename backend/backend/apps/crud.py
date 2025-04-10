from sqlmodel import Session, select

from backend.apps.models import App, AppCreate


def create_app(*, session: Session, app_create: AppCreate) -> App:
    db_obj = App.model_validate(app_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
