import random
from decimal import Decimal
from typing import List

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


class WebhooksManagerInput(BaseModel):
    webhook_name: str = Field(
        ...,
        examples=['Your application'],
        description="The Type of WebhooksManager"
    )
    endpoint: str = Field(
        None,
        examples=['https://youapplocation/webhook/endpoint'],
        description="Description of the room type."
    )
    catch_path: str = Field(
        None,
        examples=["/api/order/"],
        description="Current price. If you deploy a price controller, this value will be updated automatically."
    ),
    catch_method: List = Field(
        "*",
        description="List of HTTP methods to catch. Not case sensitive. "
                    "`*` to select all HTTP methods, separate multiple methods with commas e.g.`GET,POST`.",
        examples=["POST", "GET"],
    )


class WebhooksManager(WebhooksManagerInput, StayForgeModel):
    pass
