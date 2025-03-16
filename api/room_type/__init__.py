"""
room_type
"""
import database
import settings

from .models import RoomTypeBase
from .. import APIMongoRepository

collection_name = 'room_type'

repository = APIMongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client,
    model_class=RoomTypeBase
)
