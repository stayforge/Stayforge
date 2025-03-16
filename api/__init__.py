import os

import redis

import settings
from repository import MongoRepository


class APIMongoRepository(MongoRepository):
    def __init__(self, database, collection, client, model_class=None):
        super().__init__(database, collection, client)
        self.database = database
        self.collection = collection
        self.client = client
        self.model_class = model_class


class RedisClient:
    def __init__(self, path: str = "stayforge"):
        self.redis_url = os.path.join(settings.REDIS_URL, path)
        self.client = redis.StrictRedis.from_url(self.redis_url)
