"""
Stayforge API v1
"""
from typing import *

from pydantic import BaseModel

from api.room import repository as room
from api.room_type import repository as room_type
from api.order import repository as order

# Register the API repositories here.
repositories = {
    'room_type': room_type,
    'room': room,
    'order': order
}

# Dynamic generation of model_classes
model_classes: Dict[str, Type[BaseModel]] = {
    name: repo.model_class for name, repo in repositories.items()
}
