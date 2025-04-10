from fastapi import APIRouter

from apps.auth import auth_router
from apps.users import user_router
from apps.apps import apps_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(apps_router, prefix="/apps", tags=["Apps"])
