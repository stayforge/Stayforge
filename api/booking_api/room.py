import asyncio
import json
from datetime import datetime

import orjson
from bson import ObjectId

from api.room import get_room_by_branch
from api.room_type import get_roomType_by_branch


# Custom default conversion function to handle ObjectId and datetime
def orjson_default(obj):
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
