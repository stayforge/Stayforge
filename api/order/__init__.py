"""
order
"""
from datetime import datetime
import settings
from api.mongo_client import db

order_types: list = list(settings.ORDER_TYPE.keys())

collection_name = 'order'

db[collection_name].create_index("num", unique=False)
db[collection_name].create_index("customer_username", unique=False)
db[collection_name].create_index("room_name", unique=False)