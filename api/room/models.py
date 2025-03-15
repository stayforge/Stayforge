"""
Room Models
"""

from random import randint

from bson import ObjectId
from pydantic import BaseModel, Field

from api.schemas import StayForgeModel


class RoomBase(BaseModel):
    key_id: str = Field(
        str(ObjectId()), description="Reference ID of the key."
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
        ...,
        description="Stayforge will prioritize rooms with high priority numbers to guests. "
                    "When the priority is the same, it is randomly selected according to certain rules."
    )


class Room(RoomBase, StayForgeModel):
    pass
