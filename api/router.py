from fastapi import APIRouter

from api.healthcheck.view import router as healthcheck
from api.branch.view import router as branch
from api.order.view import router as order
from api.room.view import router as room
from api.room_type.view import router as room_type
from api.key_manager.view import router as key_manager
from api.webhooks_manager.view import router as webhooks_manager
from api.plugins_manager.view import router as plugins_manager

router = APIRouter()

router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"], include_in_schema=False)
router.include_router(webhooks_manager, prefix="/webhooks_manager", tags=["Webhooks Manager"])
router.include_router(plugins_manager, prefix="/plugins_manager", tags=["Plugins Manager"])
router.include_router(branch, prefix="/branch", tags=["Branches"])
router.include_router(room, prefix="/room", tags=["Rooms"])
router.include_router(room_type, prefix="/room_type", tags=["Room Types"])
router.include_router(order, prefix="/order", tags=["Orders"])
router.include_router(key_manager, prefix="/key", tags=["Key Manager"])
