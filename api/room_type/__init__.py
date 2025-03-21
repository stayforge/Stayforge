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
async def get_roomType_by_branch(branch_name: str):
    """
    Get all room types for a specific branch.
    If branch_name is a list in the database, this will match if the branch_name is in that list.
    """
    query = {"branch": {"$in": [branch_name]}}  # This will match if branch_name is in the list
    cursor = db[collection_name].find(query)
    return await cursor.to_list(None)

async def get_roomType_by_name(room_type_name: str):
    query = {"name": room_type_name}
    cursor = db[collection_name].find(query)
    return await cursor.to_list(None)
