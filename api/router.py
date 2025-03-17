"""
API Routers
"""
from fastapi import APIRouter, Depends
from fastapi_crudrouter_mongodb import CRUDRouter

from api import db, branch, auth, order
from api.auth import ServiceAccount
from api.auth.authenticate_view import router as auth_router
from api.auth.role import role
from api.branch.models import Branch
from api.order.models import Order
from api.room.models import Room
from api.room_type.models import RoomType

router = APIRouter()

# router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"], include_in_schema=False)
# router.include_router(webhooks_manager, prefix="/webhooks", tags=["Webhooks Manager"])
# router.include_router(models_manager, prefix="/models", tags=["Models Manager"])
# router.include_router(models_etcd, prefix="/models", tags=["Models Etcd"])
# router.include_router(mq, prefix="/mq", tags=["Message Queue"])

# Auth API
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# API v1
router.include_router(CRUDRouter(
    model=ServiceAccount,
    db=db,
    collection_name=auth.collection_name,
    prefix="/service_accounts",
    tags=["Service Accounts"],
))
router.include_router(CRUDRouter(
    model=Branch,
    db=db,
    collection_name=branch.collection_name,
    prefix="/branch",
    tags=["Branches"]
),
    dependencies=[Depends(role("Branches".lower()))]
)
router.include_router(CRUDRouter(
    model=RoomType,
    db=db,
    collection_name=branch.collection_name,
    prefix="/room_type",
    tags=["RoomTypes"]
),
    dependencies=[Depends(role("RoomTypes".lower()))]
)
router.include_router(CRUDRouter(
    model=Room,
    db=db,
    collection_name=branch.collection_name,
    prefix="/room",
    tags=["Rooms"],
),
    dependencies=[Depends(role("Rooms".lower()))]
)
router.include_router(CRUDRouter(
    model=Order,
    db=db,
    collection_name=order.collection_name,
    prefix="/order",
    tags=["Orders"],
),
    dependencies=[Depends(role("Orders".lower()))]
)
