"""
"""
import os
import uuid

import database
import settings
from api import MongoRepository
from api.auth.service_account import ServiceAccountBase, ServiceAccount

# Service Account
DEFAULT_ACCOUNT = os.getenv(
    "DEFAULT_SERVICE_ACCOUNT", "root@aim.auth.stayforge.io"
)
DEFAULT_ACCOUNT_SECRET = os.getenv(
    "DEFAULT_SERVICE_ACCOUNT_SECRET", uuid.uuid4()
)

sa_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection='service_account',
    client=database.client,
    model_class=ServiceAccount
)

# AIM
aim_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection='aim_role',
    client=database.client,
    model_class=ServiceAccount
)
