from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.apps import services
from src.apps.models import App
from src.apps.schemas import AppCreate, AppRead
from src.database.session import get_db

router = APIRouter(prefix="/api/v1/apps", tags=["Applications"])


@router.post("/", response_model=AppRead, status_code=status.HTTP_201_CREATED)
async def create_app(app: AppCreate, db: Session = Depends(get_db)):
    db_app = db.exec(select(App).where(App.name == app.name)).first()
    if db_app:
        raise HTTPException(status_code=400, detail="App already registered")
    db_app = services.create_app(db=db, app=app)
    return db_app


@router.get("/", response_model=List[App])
async def read_apps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    apps = services.get_apps(db, skip=skip, limit=limit)
    return apps
