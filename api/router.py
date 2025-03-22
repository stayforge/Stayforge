"""
API Routers
"""
from fastapi import APIRouter, Depends
from fastapi_crudrouter_mongodb import CRUDRouter

from api import branch, order, room_type, room, customer
import auth
from auth import ServiceAccount
from auth.role import role
from api.branch.models import Branch
from api.field_based_crud_router import FieldBasedCRUDRouter
from api.mongo_client import db
from api.order.models import Order
from api.room.models import Room
from api.room_type.models import RoomType
from api.customer.models import Customer

router = APIRouter()

# router.include_router(healthcheck, prefix="/healthcheck", tags=["Healthcheck"], include_in_schema=False)
# router.include_router(webhooks_manager, prefix="/webhooks", tags=["Webhooks Manager"])
# router.include_router(models_manager, prefix="/models", tags=["Models Manager"])
# router.include_router(models_etcd, prefix="/models", tags=["Models Etcd"])
# router.include_router(mq, prefix="/mq", tags=["Message Queue"])

# API v1
router.include_router(CRUDRouter(
    model=ServiceAccount,
    db=db,
    collection_name=auth.collection_name,
    prefix="/service_accounts",
    tags=["Service Accounts"],
))

router.include_router(
    FieldBasedCRUDRouter(
        model=Branch,
        db=db,
        collection_name=branch.collection_name,
        identifier_field="name",  # Use name as the identifier
        prefix="/branch",
        tags=["Branches"]
    ),
    dependencies=[Depends(role("Branches"))]
)
router.include_router(
    FieldBasedCRUDRouter(
        model=RoomType,
        db=db,
        collection_name=room_type.collection_name,
        identifier_field="name",
        prefix="/room_type",
        tags=["Room Types"],
    ),
    dependencies=[Depends(role("RoomTypes"))]
)
router.include_router(CRUDRouter(
    model=Room,
    db=db,
    collection_name=room.collection_name,
    prefix="/room",
    tags=["Rooms"]
),
    dependencies=[Depends(role("Rooms"))]
)
router.include_router(
    FieldBasedCRUDRouter(
        model=Customer,
        db=db,
        collection_name=customer.collection_name,
        identifier_field="email",
        prefix="/customer",
        tags=["Customers"]
    ),
    dependencies=[Depends(role("Customers"))]
)

router.include_router(
    FieldBasedCRUDRouter(
        model=Order,
        db=db,
        collection_name=order.collection_name,
        identifier_field="num",
        prefix="/order",
        tags=["Orders"]
    ),
    dependencies=[Depends(role("Orders"))]
)
