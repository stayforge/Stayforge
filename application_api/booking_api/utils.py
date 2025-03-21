"""
Utility functions for booking API
"""
from datetime import datetime
from bson import ObjectId

import asyncio
import json

import orjson

from api.order import get_orders_in_timeRange_by_roomType
from api.room import get_room_by_branch, get_room_by_roomType
from api.room_type import get_roomType_by_branch, get_roomType_by_name


def orjson_default(obj):
    """Custom default conversion function to handle ObjectId and datetime"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable") 


async def get_rooms_data(branch_name: str) -> dict:
    # Concurrently fetch room types and room data
    room_types, rooms = await asyncio.gather(
        get_roomType_by_branch(branch_name),
        get_room_by_branch(branch_name)
    )

    # Construct room_type mapping, key is the "name" field of room_type
    room_type_map = {rt["name"]: rt for rt in room_types if "name" in rt}

    # Group by room_type, categorize matching rooms
    data = [
        {
            "room_type": rt,
            "rooms": [room for room in rooms if room.get("room_type_name") == rt_name]
        }
        for rt_name, rt in room_type_map.items()
    ]

    result = {
        "data": data,
        "row": {
            "rooms": rooms,
            "room_types": room_types
        }
    }

    # Format output using orjson and convert to Python object via json.loads
    return json.loads(
        orjson.dumps(result, option=orjson.OPT_INDENT_2, default=orjson_default).decode()
    )

async def get_roomType_timetable(room_type_name: str, start_time: datetime, end_time: datetime) -> dict:
    # Validate if room type exists
    room_type = await get_roomType_by_name(room_type_name)
    if not room_type:
        raise ValueError(f"Room type '{room_type_name}' does not exist")

    # Concurrently fetch room types and room data
    rooms, orders = await asyncio.gather(
        get_room_by_roomType(room_type_name),
        get_orders_in_timeRange_by_roomType(room_type_name, start_time, end_time)
    )
    
    data = [
        
    ]

    result = {
        "data": data,
        "row": {
            "rooms": rooms,
            "orders": orders
        }
    }
    
    print(result)

    # Format output using orjson and convert to Python object via json.loads
    return json.loads(
        orjson.dumps(result, option=orjson.OPT_INDENT_2, default=orjson_default).decode()
    )
