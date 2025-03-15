"""
Booking API View
"""
import random
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.post("/schedule/{branch_id}", description="Return to a branch's room schedule.")
async def schedule(
        branch_id: str
):
    return


@router.post("/hold/{room_id}", description="Keep a room for x seconds, place it during this period to be booked.")
async def hold(
        room_id: str, hold_time: int
):
    return


@router.post("/booking/{room_id}", description="Book a room. Make a new order and status it to 'booked'."
                                               "If the order number is not defined, it will be created and returned by Stayforge.")
async def booking(
        room_id: str,
        order_num: str = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
):
    return


@router.post("/cancel/{order_num}", description="You can only cancel a room in booked state. "
                                                "If the room is check-in, please follow the normal check-out process.")
async def cancel(
        order_num: str
):
    return


@router.post("/check-in/{order_num}", description="Book a room. Make a new order and status it to 'booked'.")
async def check_in(
        order_num: str
):
    return


@router.post("/check-out/{order_num}", description="Book a room. Make a new order and status it to 'booked'.")
async def check_out(
        order_num: str
):
    return
