from random import randint

from bson import ObjectId
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


class RoomInput(BaseModel):
    branch_id: str = Field(
        str(ObjectId()), description="Reference ID of the branch."
    )
    room_type_id: str = Field(
        str(ObjectId()), description="Reference ID of the RoomType."
    )
    number: str = Field(
        ...,
        examples=[f"{randint(1, 9)}0{randint(1, 9)}"],
        description="The number of rooms, e.g., 203."
    )
    priority: int = Field(
        ..., description="The OTA system will give priority to rooms with a higher value to guests. "
                         "If the priorities are the same, then it is random."
    )


class Room(RoomInput, StayForgeModel):
    pass
