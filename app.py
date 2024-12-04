from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.middleware import Middleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import settings
from api import router as api_router
from docs import docs as docs

from webhook.middleware import WebhooksMiddleware

middleware = [
    Middleware(WebhooksMiddleware)
]
with open('description.md', 'r', encoding='utf-8') as file:
    description = file.read()

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
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    import json

    with open("openapi.json", "w") as f:
        api_spec = app.openapi()
        f.write(json.dumps(api_spec))
    exit(0)
