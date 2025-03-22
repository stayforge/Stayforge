import json
import uuid
from datetime import datetime, timedelta
from typing import List

from bson import ObjectId
from faker import Faker
from pydantic import BaseModel, Field, field_validator, constr

import settings
from api.order import order_types
from api.schemas import StayForgeModel

faker = Faker('ja_JP')

# noinspection PyNestedDecorators
class OrderBase(BaseModel):
    num: constr(pattern=r'^[A-Za-z0-9_\-#@:\/|\\\[\]\(\)\{\}<>\.!\?]+$') = Field(
        ...,
        examples=[f"{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int % 10000).zfill(4)}"],
        description="Order number. Only `A-Z`, `a-z`, `0-9` and `-_#@:` are allowed."
    )
    room_name: str = Field(
        None,
        examples=[str(ObjectId())],
        description="Room name"
    )
    type: str = Field(
        ...,
        examples=order_types,
        description="OrderType",
    )
    customer_username: str = Field(
        None,
        examples=['customer_name01'],
        description="Customer username"
    )
    checkin_at: datetime = Field(
        None,
        examples=[datetime.now() + timedelta(days=1)],
        description="The `start time` of this room being occupied."
    )
    checkout_at: datetime = (
        Field(
            None,
            examples=[datetime.now() + timedelta(days=2)],
            description="The `end time` of this room being occupied."
        )
    )

    @field_validator("type", mode="before")
    @classmethod
    def validate_order_type(cls, value):
        if value not in order_types:
            raise ValueError(f"OrderType Must be one of them: {json.dumps(order_types, ensure_ascii=False)}")
        return value

    @classmethod
    def generate_num(cls) -> str:
        return f"ON-{datetime.now().strftime('%Y%m%d')}-{''.join([str(uuid.uuid4().int % 10) for _ in range(10)])}"


class Order(OrderBase, StayForgeModel):
    @classmethod
    def order_types(cls) -> dict | List[str]:
        _status = settings.ORDER_TYPE
        return _status
