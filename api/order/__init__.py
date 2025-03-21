"""
order
"""
from datetime import datetime
import settings
from api.mongo_client import db

order_types: list = list(settings.ORDER_TYPE.keys())

collection_name = 'order'

db[collection_name].create_index("num", unique=True)

async def get_orders_in_timeRange_by_roomType(room_type_name: str, start_time: datetime, end_time: datetime):
    # Get rooms
    query = {"room_type_name": room_type_name}
    cursor_rooms = db['room'].find(query)
    rooms =  await cursor_rooms.to_list(None)

    # Get orders
    for room in rooms:
        query = {"room_id": room['_id'], "checkin_at": {"$gte": start_time}, "checkout_at": {"$lte": end_time}}
        cursor = db[collection_name].find(query)
        orders = await cursor.to_list(None)
        print(orders)
    try:
        return await cursor.to_list(None)
    except:
        return []

