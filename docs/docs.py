from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi

import settings

app = APIRouter()



@app.get("/", include_in_schema=False)
async def custom_redoc_ui_html():
    print(app)
    return get_redoc_html(
        openapi_url=settings.OPENAPI_URL,
        title=settings.TITLE,
        redoc_favicon_url=settings.FAVICON_URL,
        with_google_fonts=settings.REDOC_WITH_GOOGLE_FONTS
    )
