"""
API __init__.py
"""

import os
from warnings import deprecated

import motor.motor_asyncio
import redis

import settings
from repository import MongoRepository


class APIMongoRepository(MongoRepository):
    @deprecated("This class is deprecated and will be removed in future versions.")
    def __init__(self, database, collection, client, model_class=None):
        super().__init__(database, collection, client)
        self.database = database
        self.collection = collection
        self.client = client
        self.model_class = model_class


""" Mongodb Client Startup """

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
db = client.local
# Crate index here
db.service_account.create_index("account", unique=True)

""" Redis Client """


class RedisClient:
    def __init__(self, path: str = "stayforge"):
        self.redis_url = os.path.join(settings.REDIS_URL, path)
        self.client = redis.StrictRedis.from_url(self.redis_url)
