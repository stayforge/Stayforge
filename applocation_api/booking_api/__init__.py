"""
Stayforge Booking API api_factory

There is Application-level API.
Used to simplify the Order operation process of Stayforge, and facilitate handling of hold, booking, cancel booking, checkin, checkout requirements.
You can directly connect with the reservation system, reservation website, etc.
"""
from datetime import datetime

from bson import ObjectId

# Custom default conversion function to handle ObjectId and datetime

def orjson_default(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
