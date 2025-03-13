"""
Room Type Views
"""

from fastapi import APIRouter, HTTPException
from models import room_repository, RoomTypeBase, RoomType  # 确保路径正确
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/rooms/", response_model=List[RoomType])
async def get_rooms():
    rooms = await room_repository.find_many({})
    for room in rooms:
        room["id"] = str(room["_id"])
    return rooms

@router.get("/rooms/{room_id}", response_model=RoomType)
async def get_room(room_id: str):
    room = await room_repository.find_one({"_id": ObjectId(room_id)})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room["id"] = str(room["_id"])
    return room

@router.post("/rooms/", response_model=RoomType)
async def create_room(room: RoomTypeBase):
    new_room = room.dict()
    result = await room_repository.insert_one(new_room)
    new_room["id"] = str(result.inserted_id)
    return new_room

@router.put("/rooms/{room_id}", response_model=RoomType)
async def update_room(room_id: str, room: RoomTypeBase):
    update_result = await room_repository.update_one(
        {"_id": ObjectId(room_id)},
        {"$set": room.dict(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Room not found or no update needed")
    updated_room = await room_repository.find_one({"_id": ObjectId(room_id)})
    updated_room["id"] = str(updated_room["_id"])
    return updated_room

@router.delete("/rooms/{room_id}")
async def delete_room(room_id: str):
    delete_result = await room_repository.delete_one({"_id": ObjectId(room_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}