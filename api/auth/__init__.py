"""
"""
from passlib.context import CryptContext

import database
import settings
from api.auth.service_account import ServiceAccount
from repository import MongoRepository


repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection='service_account',
    client=database.client,
    model_class=ServiceAccount
)


async def ensure_indexes():
    """Create unique index"""
    await repository.collection.create_index(
        [("account", 1)],
        unique=True,
        background=True
    )


async def create_superuser():
    existing_user = await repository.collection.find_one({"account": settings.SUPERUSER_ACCOUNT_NAME})

    if existing_user:
        settings.logger.info(f"Superuser `{settings.SUPERUSER_ACCOUNT_NAME}` already exists.")
        return

    new_superuser = ServiceAccount(
        account=settings.SUPERUSER_ACCOUNT_NAME,
        secret=settings.SUPERUSER_ACCOUNT_SECRET,
        iam=settings.SUPERUSER_ACCOUNT_IAM
    )

    await repository.collection.insert_one(new_superuser.model_dump())
    settings.logger.info(f"Superuser `{settings.SUPERUSER_ACCOUNT_NAME}` created successfully.")
