"""
Application-level API

This is the top-level API that provides high-level functionality for applications.
It includes various sub-APIs like Booking API for different application needs.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/application")

# Import and include sub-routers
from .booking_api import router as booking_router
router.include_router(booking_router, prefix="/booking", tags=["Booking API"])