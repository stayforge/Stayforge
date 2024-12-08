import uuid

from bson import ObjectId
from fastapi import *
from httpcore import request

import database
import settings
from api.schemas import Stayforge
from repository import MongoRepository

router = APIRouter()


async def _database_healthcheck(field: str = str(uuid.uuid4())) -> dict:
    try:
        healthcheck_repository = MongoRepository(
            database=settings.DATABASE_NAME,
            collection='__healthcheck',
            client=database.client
        )

        # Step 1: Create random data
        random_data = {"_id": ObjectId(), "field": field}

        # Step 2: Insert random data
        insertion_result = await healthcheck_repository.insert_one(random_data)

        # Make sure insertion was successful
        if not insertion_result.inserted_id:
            raise ValueError("Failed to insert data")

        # Delete the entire collection
        await healthcheck_repository.collection.drop()

        # Resulting JSON response
        result = {
            "step_1": "Random data created",
            "step_2": "Data inserted and collection dropped",
        }
        return result
    except Exception as e:
        return {"error": str(e)}


@router.get("/", responses={"200": {"description": "pong"}}, description="ping! pong! ping!ping!ping!......pong?")
async def ping():
    return "pong"


@router.get("/info", response_model=Stayforge, description="Stayforge API Info")
async def info():
    return Stayforge()


@router.get("/database", description="Stayforge API Info")
async def db():
    return await _database_healthcheck()
