from typing import List

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

import settings
from models import RoomType, RoomTypeBase

app = FastAPI()

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]
roomType_collection = db["room_type"]


@app.post("/rooms/", response_model=RoomType)
async def create_roomType(roomType: RoomTypeBase):
    new_roomType = roomType.model_dump()
    result = await roomType_collection.insert_one(new_roomType)
    new_roomType["id"] = str(result.inserted_id)
    return new_roomType


@app.get("/rooms/", response_model=List[RoomType])
async def get_roomTypes():
    roomTypes = await roomType_collection.find().to_list(100)
    for roomType in roomTypes:
        roomType["id"] = str(roomType["_id"])
    return roomTypes


@app.get("/roomTypes/{roomType_id}", response_model=RoomType)
async def get_roomType(roomType_id: str):
    roomType = await roomType_collection.find_one({"_id": ObjectId(roomType_id)})
    if not roomType:
        raise HTTPException(status_code=404, detail="Room not found")
    roomType["id"] = str(roomType["_id"])
    return roomType


@app.put("/roomTypes/{roomType_id}", response_model=RoomType)
async def update_roomType(roomType_id: str, roomType: RoomTypeBase):
    update_result = await roomType_collection.update_one(
        {"_id": ObjectId(roomType_id)},
        {"$set": roomType.model_dump(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Room not found or no update needed")
    updated_roomType = await roomType_collection.find_one({"_id": ObjectId(roomType_id)})
    updated_roomType["id"] = str(updated_roomType["_id"])
    return updated_roomType


@app.delete("/roomTypes/{roomType_id}")
async def delete_roomType(roomType_id: str):
    delete_result = await roomType_collection.delete_one({"_id": ObjectId(roomType_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}
