from fastapi import APIRouter

from api.branch import router as branch
from api.healthcheck import router as healthcheck
from api.models_manager import etcd_router as models_etcd
from api.models_manager import router as models_manager
from api.mq import router as mq
from api.v1.view import router as v1
from api.webhooks_manager import router as webhooks_manager

router = APIRouter()

# API v1
router.include_router(v1, prefix="/v1")

router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"], include_in_schema=False)
router.include_router(branch, prefix="/branch", tags=["Branches"])
router.include_router(webhooks_manager, prefix="/webhooks", tags=["Webhooks Manager"])
router.include_router(models_manager, prefix="/models", tags=["Models Manager"])
router.include_router(models_etcd, prefix="/models", tags=["Models Etcd"])
router.include_router(mq, prefix="/mq", tags=["Message Queue"])
