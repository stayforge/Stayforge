"""
"""
import os
import uuid

import database
import settings
from api import MongoRepository
from api.auth.service_account import ServiceAccount

# Service Account
DEFAULT_ACCOUNT = os.getenv(
    "DEFAULT_SERVICE_ACCOUNT", "root@iam.auth.stayforge.io"
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
