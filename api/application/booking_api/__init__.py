"""
Stayforge Booking API

Part of the Application-level API that handles all booking-related operations.
Used to simplify the Order operation process of Stayforge, and facilitate handling of hold, booking, cancel booking, checkin, checkout requirements.
You can directly connect with the reservation system, reservation website, etc.
"""
from fastapi import APIRouter

router = APIRouter()

# Import views to register routes
from . import views  # This is important to register the routes
