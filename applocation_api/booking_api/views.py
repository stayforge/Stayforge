"""
Booking API View
"""
import random
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from fastapi import HTTPException, Query
from pydantic import BaseModel
from starlette.responses import JSONResponse

from . import router
from .room import get_rooms_data


class RoomResponse(BaseModel):
    data: List[Dict[str, Any]]
    row: Dict[str, List[Dict[str, Any]]]


class BookingResponse(BaseModel):
    success: bool
    message: str
    order_num: str | None = None


@router.get("/rooms/{branch_name}", 
    response_model=RoomResponse,
    description="Return to a branch's all room_type and room.")
async def branch_rooms(
    branch_name: str,
    start_time: Optional[datetime] = Query(None, description="Start time for filtering room types"),
    end_time: Optional[datetime] = Query(None, description="End time for filtering room types")
):
    return await get_rooms_data(branch_name, start_time, end_time) 