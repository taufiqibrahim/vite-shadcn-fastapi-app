from contextlib import asynccontextmanager
from fastapi import FastAPI

# Middlewares
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Core
from src.core.config import settings
from src.core.logging import get_logger, setup_logging

# Endpoints
from src.auth.api.v1 import endpoints as auth_endpoints_v1
from src.users.api.v1 import endpoints as users_endpoints_v1
from src.apps.api.v1 import endpoints as apps_endpoints_v1
from src.files.api.v1 import endpoints as files_endpoints_v1
from src.geospatial_mapping.api.v1 import endpoints as geospatial_mapping_endpoints_v1

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    # lifespan=lifespan,
)

# GZIP middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include the authentication and users routers
app.include_router(auth_endpoints_v1.router)
app.include_router(users_endpoints_v1.router)

# Include more routers
app.include_router(apps_endpoints_v1.router)
app.include_router(files_endpoints_v1.router)
app.include_router(geospatial_mapping_endpoints_v1.router)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
logger.warning(f"BACKEND_CORS_ORIGINS={settings.BACKEND_CORS_ORIGINS}")
logger.warning(f"FRONTEND_HOST={settings.FRONTEND_HOST}")


@app.get("/health", tags=["Default"])
def health_check():
    return {"project_name": settings.PROJECT_NAME, "status": "ok"}
