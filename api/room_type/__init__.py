"""
room_type
"""

from typing import Optional

from fastapi import Request

from .models import RoomTypeBase
from api.mongo_client import db

collection_name = 'room_type'

db[collection_name].create_index("name", unique=True)

# room_type methods
async def get_roomType_by_branch(branch_name: str, request: Optional[Request] = None):
    query = {}
    room_type_cursor = db[collection_name].find(query)
    room_type = await room_type_cursor.to_list(None)
    return room_type
