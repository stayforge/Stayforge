"""
order
"""
from faker import Faker

import database
import settings
from .. import MongoRepository
from .models import OrderBase


collection_name = 'order'

repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

faker = Faker('ja_JP')

async def create_unique_index() -> str:
    return await database[collection_name].create_index("name", unique=True)

