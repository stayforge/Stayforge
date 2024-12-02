from pydantic import BaseModel, Field

import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

collection_name = 'room'

room_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)


class Room(BaseModel):
    branch_id: str = Field(
        None, description="Reference ID of the branch."
    )
    room_type_id: str = Field(
        "", description="Reference ID of the RoomType."
    )
    number: str = Field(
        ..., description="The number of rooms, e.g., 203."
    )
    priority: int = Field(
        ..., description="The OTA system will give priority to rooms with a higher value to guests. "
                         "If the priorities are the same, then it is random."
    )


class RoomInput(Room, StayForgeModel):
    pass


async def create_unique_index():
    try:
        result = await database[collection_name].create_index("name", unique=True)
        print(f"Unique index created: {result}")
    except Exception as e:
        print(f"Error creating unique index: {e}")
