"""
room
"""
from typing import Optional

from fastapi import Request

from api import mongo_client
from .models import RoomBase
from ..mongo_client import db

collection_name = 'room'

db[collection_name].create_index("name", unique=True)


async def get_room_by_roomType(room_type_name: str, request: Optional[Request] = None):
    query = {"room_type_name": room_type_name}
    room_cursor = mongo_client.db[collection_name].find(query)
    rooms = await room_cursor.to_list(None)
    return rooms


async def get_room_by_branch(branch_name: str, request: Optional[Request] = None):
    query = {"branch_name": branch_name}
    room_cursor = mongo_client.db[collection_name].find(query)
    rooms = await room_cursor.to_list(None)
    return rooms
