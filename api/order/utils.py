from datetime import datetime
from api.order.models import Order
from . import collection_name
from api.mongo_client import db


async def get_orders_in_timeRange_by_roomType(room_type_name: str, start_time: datetime, end_time: datetime):
    # Get rooms
    query = {"room_type_name": room_type_name}
    cursor_rooms = db['room'].find(query)
    rooms =  await cursor_rooms.to_list(None)

    # Get orders
    result = []
    for room in rooms:
        query = {"room_id": room['_id'], "checkin_at": {"$gte": start_time}, "checkout_at": {"$lte": end_time}}
        cursor = db[collection_name].find(query)
        orders = await cursor.to_list(None)
        result.extend(orders)
    return result

async def create_order(order: Order) -> Order:
    """
    Create a new order in the database
    
    Args:
        order (Order): The order object to create
        
    Returns:
        Order: The created order with MongoDB _id
        
    Raises:
        DuplicateKeyError: If the order number already exists
    """
    order_dict = order.model_dump(exclude={'id'})
    result = await db[collection_name].insert_one(order_dict)
    order_dict['_id'] = result.inserted_id
    return Order(**order_dict)

