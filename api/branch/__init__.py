"""
Branch API
"""

from .models import BranchBase
from ..mongo_client import db

collection_name = 'branch'

db[collection_name].create_index("name", unique=True)
