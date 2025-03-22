"""
Booking API View
"""
import random
from datetime import datetime, timezone
from typing import List, Dict, Any

from pydantic import BaseModel
from api.order.models import Order
from api.order.utils import create_order as create_order_db

from . import router
from .utils import get_roomType_timetable, get_rooms_data


class RoomResponse(BaseModel):
    data: List[Dict[str, Any]]
    row: Dict[str, List[Dict[str, Any]]]


class BookingResponse(BaseModel):
    success: bool
    message: str
    order_num: str | None = None


class CreateOrderRequest(BaseModel):
    room_name: str
    type: str
    checkin_at: datetime
    checkout_at: datetime
    num: str | None = None


@router.get("/rooms/{branch_name}",
    response_model=RoomResponse,
    description="Return to a branch's all room_type and room.")
async def branch_rooms(branch_name: str):
    return await get_rooms_data(branch_name)


@router.get("/schedule/{room_type_name}",
    response_model=Dict[str, Any],
    description="Return to a room type's schedule.")
async def branch_schedule(room_type_name: str, start_time: datetime, end_time: datetime):
    return await get_roomType_timetable(room_type_name, start_time, end_time)


@router.post("/hold/{room_id}",
    response_model=BookingResponse,
    description="Keep a room for x seconds, place it during this period to be booked.")
async def hold(room_id: str, hold_time: int):
    return BookingResponse(
        success=True,
        message=f"Room {room_id} held for {hold_time} seconds"
    )


@router.post("/booking/{room_id}",
    response_model=BookingResponse,
    description="Book a room. Make a new order and status it to 'booked'. "
                "If the order number is not defined, it will be created and returned by Stayforge.")
async def booking(
    room_id: str,
    order_num: str=None
):
    if not order_num:
        order_num = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
    
    return BookingResponse(
        success=True,
        message=f"Room {room_id} booked successfully",
        order_num=order_num
    )


@router.post("/cancel/{order_num}",
    response_model=BookingResponse,
    description="You can only cancel a room in booked state. "
                "If the room is check-in, please follow the normal check-out process.")
async def cancel(order_num: str):
    return BookingResponse(
        success=True,
        message=f"Order {order_num} cancelled successfully"
    )


@router.post("/create_order",
    response_model=BookingResponse,
    description="Create a new order with booking details.")
async def create_order(request: CreateOrderRequest):
    try:
        # Generate order number if not provided
        if not request.num:
            request.num = Order.generate_num()
        
        # Create order object
        order = Order(
            num=request.num,
            room_name=request.room_name,
            type=request.type,
            checkin_at=request.checkin_at,
            checkout_at=request.checkout_at
        )
        
        # Save to database
        created_order = await create_order_db(order)
        
        return BookingResponse(
            success=True,
            message="Order created successfully",
            order_num=created_order.num
        )
    except Exception as e:
        return BookingResponse(
            success=False,
            message=f"Failed to create order: {str(e)}"
        )


@router.post("/check-in/{order_num}",
    response_model=BookingResponse,
    description="Check in for a booked room.")
async def check_in(order_num: str):
    return BookingResponse(
        success=True,
        message=f"Order {order_num} checked in successfully"
    )


@router.post("/check-out/{order_num}",
    response_model=BookingResponse,
    description="Check out from a room.")
async def check_out(order_num: str):
    return BookingResponse(
        success=True,
        message=f"Order {order_num} checked out successfully"
    )
