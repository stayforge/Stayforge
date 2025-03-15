import uuid
from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from faker import Faker
from pydantic import BaseModel, Field, AnyUrl

from api.schemas import StayForgeModel

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


class OrderBase(BaseModel):
    num: str = Field(..., examples=["202311151300011234"], description="Order number")
    room_id: str = Field(None, examples=[str(ObjectId())], description="Room ID")
    guest: Guest = Field(None, description="Guest information")
    type: str = Field(..., examples=['booked'], description="OrderType")
    checkin_at: datetime = Field(None, description="這個房間被佔用的開始時間。")
    checkout_at: datetime = Field(None, description="這個房間被佔用的結束時間。")

    @classmethod
    def generate_num(cls) -> str:
        return f"ON-{datetime.now().strftime('%Y%m%d')}-{''.join([str(uuid.uuid4().int % 10) for _ in range(10)])}"


class Order(OrderBase, StayForgeModel):
    @classmethod
    def order_types(cls, simple_list=False) -> List[dict]:
        _status = [
            {
                'booked': {
                    "description": "Create this order means that the room is booked. "
                                   "If checkout_at is exceeded and there is no in-using state, it will automatically be converted to close."
                }
            },
            {
                'in-using': {"description": "Create this order means that the room is in-using. "
                                            "If checkout_at is exceeded, it will automatically be converted to wait-for-maintain"
                             }
            },
            {
                'wait-for-maintain': {
                    "description": "When the guest check-out, the order will automatically change to this state. "
                                   "This state does not end automatically until the close order is created."
                }
            },
            {
                'under-maintenance': {
                    "description": "If you need to close the room for some reason, create an Order for this state. "
                                   "**It should be noted that even if you reach checkout_at, the room will not be automatically converted to close.**"
                }
            },
            {
                'close': {
                    "description": "After creating other types of orders, you must create a close order to end the room's occupation."
                }
            },
        ]
        if simple_list:
            return [__ for __ in _status]
        return _status
