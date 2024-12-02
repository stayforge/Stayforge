from fastapi import *

from api.schemas import Stayforge

router = APIRouter()


@router.get("/", responses={"200": {"description": "pong"}}, description="ping! pong! ping!ping!ping!......pong?")
async def ping():
    return "pong"


@router.get("/info", response_model=Stayforge, description="Stayforge API Info")
async def info():
    return Stayforge()
