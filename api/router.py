from fastapi import APIRouter

from api.healthcheck.view import router as healthcheck
from api.branch.view import router as branch
from api.order.view import router as order
from api.room.view import router as room
from api.room_type.view import router as room_type

router = APIRouter()

router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"])
router.include_router(branch, prefix="/branch", tags=["Branches"])
router.include_router(room, prefix="/room", tags=["Rooms"])
router.include_router(room_type, prefix="/room_type", tags=["Room Types"])
router.include_router(order, prefix="/order", tags=["Orders"])
