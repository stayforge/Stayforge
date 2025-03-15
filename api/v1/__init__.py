"""
Stayforge API v1
"""
from typing import *

from pydantic import BaseModel

from api.auth import sa_repository as service_account
from api.branch import repository as branch
from api.order import repository as order
from api.room import repository as room
from api.room_type import repository as room_type

# Register the API repositories here.
repositories = {
    'service_account': service_account,
    'branch': branch,
    'room_type': room_type,
    'room': room,
    'order': order
}

# Dynamic generation of model_classes
model_classes: Dict[str, Type[BaseModel]] = {
    name: repo.model_class for name, repo in repositories.items()
}
