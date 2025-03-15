"""
order
"""

import database
import settings
from .models import OrderBase
from .. import MongoRepository

collection_name = 'order'

repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)


async def create_unique_index() -> str:
    return await database[collection_name].create_index("name", unique=True)
