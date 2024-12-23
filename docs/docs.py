from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html

import settings

app = APIRouter()


@app.get("/", include_in_schema=False)
async def custom_redoc_ui_html():
    return get_redoc_html(
        openapi_url=settings.OPENAPI_URL,
        title=settings.TITLE,
        redoc_favicon_url=settings.FAVICON_URL,
        with_google_fonts=settings.REDOC_WITH_GOOGLE_FONTS
    )
