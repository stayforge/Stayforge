from fastapi import *
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware

import settings
from settings import logger
from api import router as api_router
from webhook.middleware import WebhooksMiddleware
middleware = [
    Middleware(WebhooksMiddleware)
]
app = FastAPI(
    title="Stayforge API",
    description="This is a basic API description.",
    version=settings.__version__,
    docs_url="/docs",
    middleware=middleware
)

app.include_router(api_router.router, prefix="/api")
