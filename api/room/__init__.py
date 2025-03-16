"""
room
"""
import database
import settings
from .. import APIMongoRepository
from .models import RoomBase

collection_name = 'room'

repository = APIMongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client,
    model_class=RoomBase
)

