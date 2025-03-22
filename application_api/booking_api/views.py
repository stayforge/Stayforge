"""
Booking API View
"""
import random
import logging
import traceback
from datetime import datetime, timezone
from typing import List, Dict, Any

from fastapi import HTTPException
from pydantic import BaseModel
from api.order.models import Order
from api.order.utils import create_order as create_order_db

from . import router
from .utils import get_roomType_timetable, get_rooms_data


logger = logging.getLogger(__name__)


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


@router.post("/create_order",
    response_model=BookingResponse,
    description="Create a new order with booking details.",
    dependencies=[])
async def create_new_order(request: CreateOrderRequest):
    try:
        # Generate order number if not provided
        if not request.num:
            request.num = Order.generate_num()
        
        logger.info(f"Creating order with num: {request.num}, room: {request.room_name}")
        
        # Print all the order types for debugging
        logger.info(f"Available order types: {Order.order_types()}")
        logger.info(f"Request order type: {request.type}")
        
        # Create order object
        try:
            # Create current timestamp for create_at and update_at
            current_time = datetime.now()
            
            order = Order(
                num=request.num,
                room_name=request.room_name,
                type=request.type,
                checkin_at=request.checkin_at,
                checkout_at=request.checkout_at,
                create_at=current_time,
                update_at=current_time
            )
            logger.info(f"Order object created: {order}")
        except Exception as e:
            logger.error(f"Failed to create Order object: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Failed to create Order object: {str(e)}")
        
        # Save to database
        try:
            logger.info(f"Calling create_order_db with order: {order.model_dump()}")
            created_order = await create_order_db(order)
            logger.info(f"Order created successfully: {created_order}")
            
            return BookingResponse(
                success=True,
                message="Order created successfully",
                order_num=created_order.num
            )
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Failed to create order: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")
    
