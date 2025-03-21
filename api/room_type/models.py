"""
Room Type Models
"""

from typing import List, Optional

from pydantic import BaseModel, Field, constr

from api.schemas import StayForgeModel


class RoomTypeBase(BaseModel):
    parent: Optional[str] = Field(
        None,
        examples=[None, "standard", "premium"],
        description="Parent room type’s name. If set to None, it will be considered a top-level room type."
    )
    name: constr(pattern=r'^[a-z0-9_-]+$') = Field(
        ...,
        examples=["happy-room-101_myhotel"],
        description="Unique name. Only `a-z`, `0-9` and `-_` are allowed."
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
    basePrice: int = Field(
        ...,
        examples=[8000],
        description="Base price. The minimum face value is in units (such as US dollars, the minimum unit is 1 cent. Japanese yen, the minimum unit is 1 yen). If you set a price strategy, the price will automatically increase according to the strategy."
    )
    pricePolicy: str = Field(
        None,
        examples=["default"],
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


class RoomType(RoomTypeBase, StayForgeModel):
    pass
