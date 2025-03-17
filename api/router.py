"""
API Routers
"""
from fastapi import APIRouter
from fastapi_crudrouter_mongodb import CRUDRouter

from api import db
from api.auth import ServiceAccount
from api.auth.authenticate_view import router as auth

router = APIRouter()

# router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"], include_in_schema=False)
# router.include_router(webhooks_manager, prefix="/webhooks", tags=["Webhooks Manager"])
# router.include_router(models_manager, prefix="/models", tags=["Models Manager"])
# router.include_router(models_etcd, prefix="/models", tags=["Models Etcd"])
# router.include_router(mq, prefix="/mq", tags=["Message Queue"])

# Auth API
router.include_router(auth, prefix="/auth", tags=["Authentication"])

# API v1
router.include_router(CRUDRouter(
    model=ServiceAccount,
    db=db,
    collection_name="service_account",
    prefix="/service_accounts",
    tags=["Service Accounts"],
))
