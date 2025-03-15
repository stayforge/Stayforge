"""
branch
"""
from faker import Faker
from pydantic import BaseModel, Field

from api.schemas import StayForgeModel

faker = Faker('ja_JP')

class BranchBase(BaseModel):
    name: str = Field(
        ...,
        examples=[f"ホテルステイフォージ{faker.town()}"],
        description="The name of the hotel branch. By default, it combines a base name with a random town."
    )
    postcode: str = Field(
        "000-0000",
        examples=[faker.postcode()],
        description="The postal code of the branch location."
    )
    address: str = Field(
        "000-0000",
        examples=[
            f"{faker.administrative_unit()}{faker.city()}{faker.town()}{faker.chome()}{faker.ban()}{faker.gou()}"
        ],
        description="The full effective of the branch, including administrative unit, city, town, and detailed location."
    )
    telephone: str = Field(
        examples=[f"{faker.phone_number()}"],
        description="The contact telephone number for the branch."
    )


class Branch(BranchBase, StayForgeModel):
    pass
