from typing import List
from bson import ObjectId
from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class RoomTypeResponses(BaseResponses):
    data: Optional[List[RoomType]]


@router.get("/", response_model=RoomTypeResponses)
async def get_room_types(
        request: Request,
        name: str = Query(
            ..., description="The Type of RoomTypeType"),
        description: str = Query(
            None, description="Description of the room_type type"
        ),
        price: int = Query(
            ...,
            description="Current price. If you deploy a price controller, this value will be updated automatically."
        ),
        price_policy: str = Query(
            None,
            description="The price controller will modify the corresponding price field based on the price policy ID."
        ),
        price_max: int = Query(
            None, description="The max of price."),
        price_min: int = Query(
            ..., description="The min of price.")
):
    str_time = time.perf_counter()
    try:
        query = {key: value for key, value in {
            "description": description, "price": price, "price_policy": price_policy,
            "price_max": price_max, "price_min": price_min
        }.items() if value}
        ds = await room_repository.find_many(query=query, request=request)

        result = []
        for d in ds:
            result.append(RoomType.from_mongo(d))

        return RoomTypeResponses(
            data=result,
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return handle_error(e, str_time)


@router.get("/<id>", response_model=RoomTypeResponses)
async def get_room(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return RoomTypeResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        d = await room_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return RoomTypeResponses(
            data=[RoomType.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.post("/", response_model=RoomTypeResponses, responses={
    409: {
        "description": "Resource maybe created. But can't found it.",
    }
})
async def create_room(request: Request, data: RoomTypeInput):
    str_time = time.perf_counter()
    try:
        _id = await room_repository.insert_one(data.model_dump(), request=request)
        d = await room_repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return RoomTypeResponses(
            data=[RoomType.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.delete("/<id>", response_model=RoomTypeResponses)
async def delete_room(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        d = await room_repository.delete_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return RoomTypeResponses(
            data=None,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail=f"Successfully. [{d}] Resource(s) deleted."
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.put("/{id}", response_model=RoomTypeResponses, responses={
    409: {
        "description": "Resource maybe changed. But can't found it.",
    }
})
async def put_room(
        request: Request,
        id: str,
        data: RoomTypeInput
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        await room_repository.update_one(query={"_id": ObjectId(id)}, update=data.model_dump(),
                                         request=request)
        d = await room_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return RoomTypeResponses(
            data=[RoomType.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)
