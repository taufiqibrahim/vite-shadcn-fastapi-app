from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from api.dependencies import SessionDep
from apps.apps.models import App, AppsPublic


router = APIRouter()


@router.get(
    "/",
    # dependencies=[Depends(get_current_active_superuser)],
    response_model=AppsPublic,
)
def read_apps(session: SessionDep, skip: int = 0, limit: int = 10) -> Any:
    """
    Retrieve users.
    """

    count_statement = select(func.count()).select_from(App)
    count = session.exec(count_statement).one()

    statement = select(App).offset(skip).limit(limit)
    apps = session.exec(statement).all()

    return AppsPublic(data=apps, count=count)
