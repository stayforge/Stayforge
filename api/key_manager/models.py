from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field

import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

from faker import Faker

collection_name = 'key'

key_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

faker = Faker('ja_JP')


class KeyInput(BaseModel):
    url: str = Field(
        ...,
        examples=["https://qr-key.net/AFs1f"],
        description="The name of the hotel key. By default, it combines a base name with a random town."
    )
    num: str = Field(
        "",
        examples=[],
        description="Order number"
    )
    effective_at: str = Field(
        datetime.now(timezone.utc),
        description="Effective at"
    )
    ineffective_at: str = Field(

        (datetime.now(timezone.utc) + timedelta(days=1)),
        description="Ineffective at"
    )


class Key(KeyInput, StayForgeModel):
    pass
