from pydantic import BaseModel

import settings
import database
from api.schemas import StayForgeModel
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


class Branch(BranchInput, StayForgeModel):
    pass
