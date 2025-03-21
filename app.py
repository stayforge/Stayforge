import asyncio
import json
import os
from contextlib import asynccontextmanager

import aiofiles
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import settings
from docs import docs as docs
from auth import router as auth_router
from application_api import router as application_api_router
from api.router import router as api_router

from settings import logger


def load_description(file_path: str) -> str:
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(abs_path, 'r', encoding='utf-8') as file:
        return file.read()


middleware = [
    # Middleware(WebhooksMiddleware)
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: export OpenAPI JSON
    task = asyncio.create_task(export_openapi_json("openapi.json"))
    yield
    # Shutdown: ensure the task is completed
    await task


description = load_description('README.md')

app = FastAPI(
    title=settings.TITLE,
    description=description,
    version=settings.__version__,
    openapi_url='/openapi.json',
    contact={
        "name": "Stayforge Support",
        "url": "https://stayforge.io/support",
        "email": "support@stayforge.io",
    },
    middleware=middleware,
    docs_url="/docs/swagger",
    redoc_url="/docs",
    lifespan=lifespan,
)

# Auth API
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}},
)

# Application-level API (includes Booking API)
app.include_router(
    application_api_router,
    responses={401: {"description": "Unauthorized"}},
)

# Stayforge API
app.include_router(
    api_router,
    prefix="/api",
    responses={401: {"description": "Unauthorized"}},
)

# Document
app.include_router(docs.app, prefix="/docs", include_in_schema=False)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.TITLE,
        description=description,
        version=settings.__version__,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://raw.githubusercontent.com/tokujun-t/Stayforge/refs/heads/dev/docs/stayforge.png"
    }
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "Bearer",
            "bearerFormat": "JWT",
            "description": "Please use `access_token`."
        }
    }
    # Path to cover security requirements
    endpoints_to_override = [
        "/auth/authenticate",
        "/auth/refresh_access_token"
    ]

    for path, methods in openapi_schema["paths"].items():
        # If path is prefixed with either endpoints_to_override, security is empty;
        # otherwise BearerAuth is added
        security_setting = [] if any(path.startswith(ep) for ep in endpoints_to_override) else [{"BearerAuth": []}]
        for method in methods:
            methods[method]["security"] = security_setting
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


async def export_openapi_json(file_path: str):
    async with aiofiles.open(file_path, "w") as f:
        api_spec = app.openapi()
        await f.write(json.dumps(api_spec, indent=4))
    logger.info(f"OpenAPI JSON exported to {file_path}")

