"""
branch
"""

import database
import settings
from .models import BranchBase
from .. import MongoRepository

collection_name = 'branch'

repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client,
    model_class=BranchBase
)

