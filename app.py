from fastapi import FastAPI

import settings
from api import router as api_router



app = FastAPI(
    title="Stayforge API",
    description="This is a basic API description.",
    version=settings.__version__,
    docs_url="/docs"
)

app.include_router(api_router.router, prefix="/api")
