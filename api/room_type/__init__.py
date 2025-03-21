"""
room_type
"""

from typing import Optional
from datetime import datetime

from fastapi import Request

from .models import RoomTypeBase
from api.mongo_client import db

collection_name = 'room_type'

db[collection_name].create_index("name", unique=True)

# room_type methods
async def get_roomType_by_branch(branch_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    """
    Get all room types for a specific branch.
    If branch_name is a list in the database, this will match if the branch_name is in that list.
    
    Args:
        branch_name (str): The branch name to search for
        start_time (datetime, optional): Start time for filtering
        end_time (datetime, optional): End time for filtering
    """
    query = {"branch": {"$in": [branch_name]}}  # This will match if branch_name is in the list
    
    # Add time range filter if provided
    if start_time or end_time:
        query["time"] = {}
        if start_time:
            query["time"]["$gte"] = start_time
        if end_time:
            query["time"]["$lte"] = end_time
            
    cursor = db[collection_name].find(query)
    return await cursor.to_list(None)

async def get_roomType_by_name(room_type_name: str):
    query = {"name": room_type_name}
    cursor = db[collection_name].find(query)
    return await cursor.to_list(None)
