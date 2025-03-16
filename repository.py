import functools
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Callable

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient


def log_method_call(log_collection: Callable[[Any], Any]):
    def decorator(method: Callable):
        @functools.wraps(method)
        async def wrapper(self, *args, request: Optional[Request] = None, **kwargs):
            client_host = request.client.host if request else "Unknown"
            user_agent = request.headers.get("user-agent") if request else "Unknown"

            input_data = {
                "method": method.__name__,
                "args": args,
                "kwargs": kwargs,
                "client_host": client_host,
                "user_agent": user_agent,
                "called_at": datetime.now(timezone.utc),
            }

            try:
                result = await method(self, *args, request=request, **kwargs)
                input_data["output"] = str(result)
                input_data["status"] = "success"
            except Exception as e:
                input_data["output"] = str(e)
                input_data["status"] = "error"
                raise
            finally:
                log_collection_instance = log_collection(self)
                await log_collection_instance.insert_one(input_data)
            return result

        return wrapper

    return decorator


class Duplicate:
    pass


class MongoRepository:
    def __init__(self, database: str, collection: str, client: AsyncIOMotorClient,
                 log_collection: str = 'logs_method_call', model_class: Any = None):
        self.db = client[database]
        self.collection = self.db[collection]
        self.log_collection = self.db[log_collection]
        self.model_class = model_class

    @log_method_call(log_collection=lambda self: self.log_collection)
    async def insert_one(self, data: Dict[str, Any], request: Optional[Request]) -> str:
        result = await self.collection.insert_one({
            **data,
            "create_at": datetime.now(timezone.utc),
        })
        return str(result.inserted_id)

    @log_method_call(log_collection=lambda self: self.log_collection)
    async def find_one(self, query: Dict[str, Any], request: Optional[Request]) -> Optional[Dict[str, Any]]:
        document = await self.collection.find_one(filter=query)
        if document and self.model_class:
            model_instance = self.model_class(**document)
            return model_instance
        else:
            return document

    @log_method_call(log_collection=lambda self: self.log_collection)
    async def find_many(self, query: Dict[str, Any], request: Optional[Request]) -> List[Dict[str, Any]]:
        cursor = self.collection.find(query)
        documents = []
        async for doc in cursor:
            documents.append(doc)
        return documents

    @log_method_call(log_collection=lambda self: self.log_collection)
    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], request: Optional[Request]) -> int:
        update["update_at"] = datetime.now(timezone.utc)
        result = await self.collection.update_one(query, {"$set": update})
        return result.modified_count

    @log_method_call(log_collection=lambda self: self.log_collection)
    async def delete_one(self, query: Dict[str, Any], request: Optional[Request]) -> int:
        result = await self.collection.delete_one(query)
        return result.deleted_count
