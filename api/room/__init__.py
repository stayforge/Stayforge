"""
room
"""
import database
import settings
from .. import MongoRepository
from .models import RoomBase

collection_name = 'room'

repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client,
    model_class=RoomBase
)

