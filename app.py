import json
import os

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import settings
from api import router as api_router
from docs import docs as docs


def load_description(file_path: str) -> str:
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(abs_path, 'r', encoding='utf-8') as file:
        return file.read()


middleware = [
    # Middleware(WebhooksMiddleware)
]

app = FastAPI(
    openapi_url='/openapi.json',
    contact={
        "name": "Stayforge Support",
        "url": "https://stayforge.io/support",
        "email": "support@stayforge.io",
    },
    middleware=middleware,
    docs_url="/docs/swagger",
    redoc_url="/docs/redoc",
)

description = load_description('README.md')

app.include_router(api_router.router, prefix="/api")
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
        "/api/auth/authenticate",
        "/api/auth/refresh_access_token"
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


def export_openapi_json(file_path: str):
    with open(file_path, "w") as f:
        api_spec = app.openapi()
        json.dump(api_spec, f, indent=4)
    print(f"OpenAPI JSON exported to {file_path}")


if __name__ == '__main__':
    export_openapi_json("openapi.json")
