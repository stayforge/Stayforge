from typing import Any

from bson import ObjectId
from pydantic import BaseModel

import database
import settings
from api.schemas import StayForgeModel
from repository import MongoRepository


def repository(collection):
    return MongoRepository(
        database=settings.DATABASE_NAME,
        collection=collection,
        client=database.client
    )


class DBInput(BaseModel):
    document: Any


class DB(DBInput, StayForgeModel):
    _id: ObjectId

