"""
branch
"""

import database
import settings
from .models import BranchBase
from .. import APIMongoRepository

collection_name = 'branch'

repository = APIMongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client,
    model_class=BranchBase
)

