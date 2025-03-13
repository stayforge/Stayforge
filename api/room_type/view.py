"""
Room Type Views
"""

from typing import List

from bson import ObjectId
from fastapi import FastAPI, HTTPException, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

import settings
from .models import RoomType, RoomTypeBase

room_type = APIRouter()

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]
room_type_collection = db["room_type"]


@room_type.post("/rooms/", response_model=RoomType)
async def create_room_type(room_type: RoomTypeBase):
    new_room_type = room_type.model_dump()
    result = await room_type_collection.insert_one(new_room_type)
    new_room_type["id"] = str(result.inserted_id)
    return new_room_type


@room_type.get("/rooms/", response_model=List[RoomType])
async def get_room_types():
    room_types = await room_type_collection.find().to_list(100)
    for room_type in room_types:
        room_type["id"] = str(room_type["_id"])
    return room_types


@room_type.get("/room_types/{room_type_id}", response_model=RoomType)
async def get_room_type(room_type_id: str):
    room_type = await room_type_collection.find_one({"_id": ObjectId(room_type_id)})
    if not room_type:
        raise HTTPException(status_code=404, detail="Room not found")
    room_type["id"] = str(room_type["_id"])
    return room_type


@room_type.put("/room_types/{room_type_id}", response_model=RoomType)
async def update_room_type(room_type_id: str, room_type: RoomTypeBase):
    update_result = await room_type_collection.update_one(
        {"_id": ObjectId(room_type_id)},
        {"$set": room_type.model_dump(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Room not found or no update needed")
    updated_room_type = await room_type_collection.find_one({"_id": ObjectId(room_type_id)})
    updated_room_type["id"] = str(updated_room_type["_id"])
    return updated_room_type


@room_type.delete("/room_types/{room_type_id}")
async def delete_room_type(room_type_id: str):
    delete_result = await room_type_collection.delete_one({"_id": ObjectId(room_type_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}
