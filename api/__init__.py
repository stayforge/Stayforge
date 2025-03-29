"""
API
"""

import os
from deprecated import deprecated

import redis

import settings
# from api import auth, branch, room_type, room, order
from repository import MongoRepository


class APIMongoRepository(MongoRepository):
    @deprecated("This class is deprecated and will be removed in future versions.")
    def __init__(self, database, collection, client, model_class=None):
        super().__init__(database, collection, client)
        self.database = database
        self.collection = collection
        self.client = client
        self.model_class = model_class


""" Redis Client """


class RedisClient:
    def __init__(self, path: str = "stayforge"):
        self.redis_url = os.path.join(settings.REDIS_URL, path)
        self.client = redis.StrictRedis.from_url(self.redis_url)
