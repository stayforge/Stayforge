"""
room_type
"""
import database
import settings
from .. import MongoRepository
from .models import RoomTypeBase

collection_name = 'room_type'

repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client,
    model_class=RoomTypeBase
)
