from fastapi import APIRouter

from api.branch import router as branch
from api.healthcheck import router as healthcheck
from api.models_manager import router as models_manager
from api.mq import router as mq
from api.order import router as order
from api.room import router as room
from api.room_type import router as room_type
from api.webhooks_manager import router as webhooks_manager
from api.data_manager import router as data_manager

router = APIRouter()

router.include_router(branch, prefix="/branch", tags=["Branches"])
router.include_router(room, prefix="/room", tags=["Rooms"])
router.include_router(room_type, prefix="/room_type", tags=["Room Types"])
router.include_router(order, prefix="/order", tags=["Orders"])
router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"], include_in_schema=False)
router.include_router(webhooks_manager, prefix="/webhooks_manager", tags=["Webhooks Manager"])
router.include_router(models_manager, prefix="/models_manager", tags=["Models Manager"])
router.include_router(mq, prefix="/mq", tags=["Message Queue"])
router.include_router(data_manager, prefix="/db", tags=["Data Manager"])
