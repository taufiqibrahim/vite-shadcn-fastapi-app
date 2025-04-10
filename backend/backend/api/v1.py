from fastapi import APIRouter

from backend.auth import auth_router
from backend.users import user_router
from backend.apps import apps_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(apps_router, prefix="/apps", tags=["Apps"])
