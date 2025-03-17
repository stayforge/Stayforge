"""
Room Models
"""

from random import randint

from pydantic import BaseModel, Field, constr

from api.schemas import StayForgeModel


class RoomBase(BaseModel):
    room_type_id: str = Field(
        ..., description="Reference ID of the RoomType."
    )
    branch_id: str = Field(
        ..., description="Reference ID of the Branch."
    )
    number: str = Field(
        ...,
        examples=[f"{randint(1, 9)}0{randint(1, 9)}"],
        description="The number of rooms, e.g., 203."
    )
    name: constr(pattern=r'^[a-z0-9_-]+$') = Field(
        ...,
        examples=["happy-room-101_myhotel"],
        description="Unique name. Only `a-z`, `0-9` and `-_` are allowed."
    )
    name_visible: str = Field(
        None,
        examples=["Happy Room"],
        description=""
    )
    priority: int = Field(
        0,
        description="Stayforge will prioritize rooms with high priority numbers to guests. "
                    "When the priority is the same, it is randomly selected according to certain rules."
    )


class Room(RoomBase, StayForgeModel):
    pass
