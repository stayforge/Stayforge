"""
Auth
"""
from fastapi import APIRouter

from api.mongo_client import db
from auth.models import ServiceAccount

router = APIRouter()

collection_name = 'service_account'

db[collection_name].create_index("account", unique=True)

# Import views to register routes
from . import authenticate_view  # This is important to register the routes
