from fastapi import FastAPI, Depends

from api import router as api_router

app = FastAPI(
    title="Stayforge API",
    description="This is a basic API description.",
    version="1.0.0",
    docs_url="/docs"
)

app.include_router(api_router.router, prefix="/api")
