import uuid
from datetime import datetime

from bson import ObjectId
from faker.proxy import Faker
from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List

import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

collection_name = 'order'

order_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

faker = Faker('ja_JP')


class IDDocument(BaseModel):
    MRZ: str = Field(
        None,
        examples=["P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
                  "L898902C36UTO7408122F1204159ZE184226B<<<<<10"]
    )
    photocopy: Optional[AnyUrl | str] = Field(
        None,
        examples=["https://a.s3storage.address/photocopy/1970010112839010/1.jpg"]
    )


class Guest(BaseModel):
    first_name: str = Field(
        None,
        examples=[faker.first_name()],
    )
    middle_name: str = Field(
        None,
        examples=[""],
    )
    last_name: str = Field(
        None,
        examples=[faker.last_name()],
    )
    gender: str = Field(
        None,
        examples=["M", "F", "..."],
    )
    birthday: str = Field(
        None,
        examples=[faker.date_of_birth()],
    )
    nationality: str = Field(
        None,
        examples=["JPN"],
    )
    email: str = Field(
        None,
        examples=[faker.email()],
    )
    phone_number: str = Field(
        None,
        examples=[faker.phone_number()],
    )
    address: str = Field(
        None,
        examples=[faker.address()],
    )
    occupation: str = Field(
        None,
        examples=[faker.job()],
    )
    passport_number: str = Field(
        None,
        examples=["FH254787"],
    )
    id_document: Optional[IDDocument]


async def create_unique_index() -> str:
    return await database[collection_name].create_index("name", unique=True)


class OrderInput(BaseModel):
    num: str = Field(create_unique_index(), examples=["ON-20231115-1234567890"], description="Order number")
    room_id: str = Field(None, examples=[str(ObjectId())], description="Room ID")
    guest: Guest = Field(None, description="Guest information")
    type: str = Field(..., examples=['booked'], description="OrderType")
    scheduled_checkin_at: datetime = Field(None, description="Creation timestamp")
    scheduled_checkout_at: datetime = Field(None, description="Creation timestamp")

    @classmethod
    def generate_num(cls) -> str:
        return f"ON-{datetime.now().strftime('%Y%m%d')}-{''.join([str(uuid.uuid4().int % 10) for _ in range(10)])}"


class Order(OrderInput, StayForgeModel):
    @classmethod
    def order_types(cls, simple_list=False) -> List[dict]:
        _ = [
            {'booked': {'room_using': False,
                        "description": "If a room is set to order and 'room_using': True, the room will be marked as in use."}},
            {'staying': {'room_using': True}},
            {'expired': {
                'room_using': True,
                'bind_datetime_col': 'scheduled_checkout_at',
                "description": "Automatically listening for orders, when the time in `bind_datetime_col` is reached,"
                               " than it will initiate a new order, type is ‘expired’"
            }},
            {'dirty': {'room_using': True,
                       "description": "The guest has exited the room. The room is being cleaned or will be cleaned soon."}},
            {'ready': {'room_using': False, "description": "Room is already for next order."}},  #
            {'plan_to_close': {
                "description": "When this room is created in the ready state, it will automatically check whether there is"
                               "this order in the history, and if so, the room will be changed to the close state. "
                               "Used for planned maintenance."}},
            {'close': {'room_using': True, "description": "Room is closing for maintenance."}},
        ]
        if simple_list:
            return [__ for __ in _]
        return _
