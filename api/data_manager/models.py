from typing import Any, TypeVar

from bson import ObjectId
from pydantic import BaseModel

import database
import settings
from api.schemas import StayForgeModel
from repository import MongoRepository

T = TypeVar("T")

def repository(collection):
    return MongoRepository(
        database=settings.DATABASE_NAME,
        collection=collection,
        client=database.client
    )