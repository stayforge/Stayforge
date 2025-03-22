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
    
    # Total number of rooms for this room type
    total_rooms = len(rooms)
    
    data = []
    
    # Generate time slices
    current_time = start_time
    time_delta = (end_time - start_time) / 24  # Dividing into 24 time slices, can be adjusted
    
    while current_time < end_time:
        slice_end = current_time + time_delta
        
        # Check orders for this time slice
        slice_orders = [
            order for order in orders 
            if (order.get("start_time") < slice_end and 
                order.get("end_time", datetime.max) > current_time)
        ]
        
        # Count occupied rooms in this time slice
        occupied_rooms = 0
        
        # Track unique room IDs to avoid counting a room twice
        occupied_room_ids = set()
        
        for order in slice_orders:
            # If the order has a room_id field, we can track which specific room is occupied
            room_id = order.get("room_id")
            
            # Skip if we've already counted this room in this time slice
            if room_id and room_id in occupied_room_ids:
                continue
                
            # Check if order is closed and checked out before this time slice
            is_available = False
            
            if order.get("type") == "close":
                check_out_time = order.get("check_out_at")
                if check_out_time and check_out_time <= current_time:
                    is_available = True
            
            # Check for expired but not closed orders
            end_time_order = order.get("end_time")
            current_datetime = datetime.now()
            if end_time_order and end_time_order < current_datetime and order.get("type") != "close":
                is_available = False
            
            # Count room as occupied if not available
            if not is_available:
                occupied_rooms += 1
                if room_id:
                    occupied_room_ids.add(room_id)
        
        # Calculate available rooms
        available_rooms = total_rooms - occupied_rooms
        if available_rooms < 0:
            available_rooms = 0  # Safeguard against negative counts
        
        # Add time slice data
        data.append({
            "start_time": current_time,
            "end_time": slice_end,
            "available_rooms": available_rooms,
            "total_rooms": total_rooms
        })
        
        current_time = slice_end

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
