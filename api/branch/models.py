
from pydantic import BaseModel
from typing import Optional

import settings
import database
from repository import MongoRepository

collection_name = 'branch'

branch_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)


class BranchInput(BaseModel):
    name: str
    address: str
    telephone: str


class Branch(BranchInput):
    id: Optional[str]

    @classmethod
    def from_mongo(cls, document: dict):
        if isinstance(document, list):
            return [cls.from_mongo(doc) for doc in document]
        if document:
            document["id"] = str(document["_id"])
            del document["_id"]
        return cls(**document)


async def create_unique_index():
    try:
        result = await database[collection_name].create_index("name", unique=True)
        print(f"Unique index created: {result}")
    except Exception as e:
        print(f"Error creating unique index: {e}")
