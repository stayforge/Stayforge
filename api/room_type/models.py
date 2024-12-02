from pydantic import BaseModel, Field

import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

collection_name = 'room_type'

room_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)


class RoomType(BaseModel):
    name: str = Field(
        ..., description="The Type of RoomType"
    )
    description: str = Field(
        None, description="Description of the room_type type"
    )
    price: int = Field(
        ..., description="Current price. If you deploy a price controller, this value will be updated automatically."
    )
    price_policy: str = Field(
        None,
        description="The price controller will modify the corresponding price field based on the price policy ID."
    )
    price_max: int = Field(
        None, description="The max of price."
    )
    price_min: int = Field(
        ..., description="The min of price."
    )


class RoomTypeInput(RoomType, StayForgeModel):
    pass


async def create_unique_index():
    try:
        result = await database[collection_name].create_index("name", unique=True)
        print(f"Unique index created: {result}")
    except Exception as e:
        print(f"Error creating unique index: {e}")
