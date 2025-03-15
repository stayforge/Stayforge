"""
Stayforge API v1
"""
from typing import *

from pydantic import BaseModel

from api.room_type import repository as room_type

# Register the API repositories here.
repositories = {
    'room_type': room_type,
}

# Dynamic generation of model_classes
model_classes: Dict[str, Type[BaseModel]] = {
    name: repo.model_class for name, repo in repositories.items()
}
