"""
Auth
"""

from api.auth.models import ServiceAccount, ServiceAccount
from api.mongo_client import db

collection_name = 'service_account'

db[collection_name].create_index("account", unique=True)
