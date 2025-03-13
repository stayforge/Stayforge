"""
Room Type Models
"""

from decimal import Decimal

from pydantic import BaseModel, Field

import database
import settings
from api.schemas import StayForgeModel
from repository import MongoRepository

collection_name = 'room_type'

room_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)


class RoomTypeBase(BaseModel):
    parent: str = Field(
        None,
        examples=[None, "standard", "premium"],
        description="Parent room type's name. When it is None, "
    )
    name: str = Field(
        ...,
        examples=['standard', 'premium'],
        description="Unique name of RoomType"
    )
    nameVisible: str = Field(
        ...,
        examples=['Standard', 'Premium'],
        description="A visible name of the room type."
    )
    description: str = Field(
        None, description="Description of the room type."
    )
    basePrice: Decimal = Field(
        ...,
        examples=[8000],
        description="Base price. If you set a price strategy, the price will automatically increase according to the strategy."
    )
    pricePolicy: str = Field(
        None,
        description="The price controller will modify the corresponding price field based on the price policy name."
    )
    min_usage: float = Field(
        8, description="Minimum usage hours."
    )
    max_usage: float = Field(
        24 * 30, description="Maximum usage hours."
    )
    allowExtension: bool = Field(
        True, description="When it True, this type will marked as allowed to extend."
    )


class RoomType(RoomTypeBase, StayForgeModel):
    pass
