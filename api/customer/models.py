"""
Customer API
"""
from faker import Faker
from pydantic import BaseModel, Field, EmailStr

from api.schemas import StayForgeModel

faker = Faker('ja_JP')

class CustomerBase(BaseModel):
    username: str = Field(
        ...,
        examples=['customer_name01'],
        description="The username of the customer.",
        pattern="^[a-z0-9_]+$"
    )   
    email: EmailStr = Field(
        None,
        examples=[faker.email()],
        description="The email of the customer."
    )
    first_name: str = Field(
        None,
        examples=[faker.first_name()],
        description="The first name of the customer."
    )
    last_name: str = Field(
        None,
        examples=[faker.last_name()],
        description="The last name of the customer."
    )

class Customer(CustomerBase, StayForgeModel):
    pass
