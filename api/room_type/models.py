"""
Room Type Models
"""

from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field

from api.schemas import StayForgeModel


class RoomTypeBase(BaseModel):
    parent: str = Field(
        None,
        examples=[None, "standard", "premium"],
        description="Parent room type’s name. If set to None, it will be considered a top-level room type."
    )
    name: str = Field(
        ...,
        examples=['standard', 'premium'],
        description="Unique name of RoomType."
    )
    nameVisible: str = Field(
        ...,
        examples=['Standard', 'Premium'],
        description="A visible name of the room type."
    )
    description: str = Field(
        None, description="Description of the room type."
    )
    branch: List[str] = Field(
        None,
        examples=[None, ["branch1", "branch2"]],
        description="Branch names that this type is available. If None, it will follow the parent settings or allow all branches by default."
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
        ..., examples=[1.5, 8],
        description="Minimum usage hours."
    )
    max_usage: float = Field(
        ..., examples=[24 * 30],
        description="Maximum usage hours."
    )
    allowExtension: bool = Field(
        default_factory=lambda: True,
        examples=[True, False],
        description="When it True, this type will marked as allowed to extend."
    )

class RoomType(StayForgeModel, RoomTypeBase):
    pass
