import uuid
from datetime import datetime

from pydantic import BaseModel, Field
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


class Guest(BaseModel):
    first_name: str = Field(None)
    middle_name: str = Field(None)
    last_name: str = Field(None)
    gender: str = Field(None)
    birthday: str = Field(None)
    nationality: str = Field(None)
    email: str = Field(None)
    phone_number: str = Field(None)
    address: str = Field(None)
    occupation: str = Field(None)
    passport: str = Field(None)
    id_photocopy: str = Field(None)


class OrderInput(BaseModel):
    num: str = Field(default_factory=lambda: OrderInput.generate_num(), description="Order number")
    room_id: str = Field(None, description="Room ID")
    guest: Guest = Field(None, description="Guest information")
    type: str = Field(..., description="OrderType")
    scheduled_checkin_at: datetime = Field(None, description="Creation timestamp")
    scheduled_checkout_at: datetime = Field(None, description="Creation timestamp")

    @classmethod
    def generate_num(cls) -> str:
        return f"ON-{datetime.now().strftime('%Y%m%d')}-{''.join([str(uuid.uuid4().int % 10) for _ in range(10)])}"


class Order(OrderInput, StayForgeModel):
    @classmethod
    def order_types(cls) -> List[dict]:
        return [
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


async def create_unique_index():
    try:
        result = await database[collection_name].create_index("name", unique=True)
        print(f"Unique index created: {result}")
    except Exception as e:
        print(f"Error creating unique index: {e}")
