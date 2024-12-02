from fastapi import APIRouter

from api.healthcheck.view import router as healthcheck
from api.branch.view import router as branch
from api.order.view import router as order

router = APIRouter()

router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"])
router.include_router(branch, prefix="/branch", tags=["Branches"])
router.include_router(order, prefix="/order", tags=["Orders"])