import random
from decimal import Decimal

from faker.proxy import Faker
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

faker = Faker('ja_JP')


class RoomTypeInput(BaseModel):
    name: str = Field(
        ...,
        examples=['スタンダード', 'プレミアム'],
        description="The Type of RoomType"
    )
    description: str = Field(
        None, description="Description of the room type."
    )
    price: Decimal = Field(
        ...,
        examples=[random.randint(8000, 50000)],
        description="Current price. If you deploy a price controller, this value will be updated automatically."
    )
    price_policy: str = Field(
        None,
        description="The price controller will modify the corresponding price field based on the price policy ID."
    )
    price_max: Decimal = Field(
        None,
        examples=[random.randint(15000, 30000)],
        description="The max of price."
    )
    price_min: Decimal = Field(
        ...,
        examples=[random.randint(7000, 12000)],
        description="The min of price."
    )


class RoomType(RoomTypeInput, StayForgeModel):
    pass
