import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware import Middleware

import settings
from api import router as api_router
from docs import docs as docs
from webhook.middleware import WebhooksMiddleware
import json


def load_description(file_path: str) -> str:
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(abs_path, 'r', encoding='utf-8') as file:
        return file.read()


middleware = [
    Middleware(WebhooksMiddleware)
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
)

description = load_description('description.md')

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
    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi


def export_openapi_json(file_path: str):
    with open(file_path, "w") as f:
        api_spec = app.openapi()
        json.dump(api_spec, f, indent=4)
    print(f"OpenAPI JSON exported to {file_path}")


if __name__ == '__main__':
    export_openapi_json("openapi.json")
    exit(0)
