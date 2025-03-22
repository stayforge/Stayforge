"""
Customer API
"""

from .models import CustomerBase
from ..mongo_client import db

collection_name = 'customer'

db[collection_name].create_index("username", unique=True)
db[collection_name].create_index("email", unique=False)