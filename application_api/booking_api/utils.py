"""
Utility functions for booking API
"""
from datetime import datetime
from bson import ObjectId


def orjson_default(obj):
    """Custom default conversion function to handle ObjectId and datetime"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable") 