from typing import List, Optional
from bson import ObjectId
from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class KeyResponses(BaseResponses):
    data: Optional[List[Key]]


@router.get("/{id}", response_model=KeyResponses)
async def get_key(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return KeyResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        d = await key_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return KeyResponses(
            data=[Key.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.get("/num/{num}", response_model=KeyResponses)
async def get_key_by_num(
        request: Request,
        num: str = Query(...)
):
    str_time = time.perf_counter()
    try:
        query = {key: value for key, value in {"num": num}.items() if value}
        ds = await key_repository.find_many(query=query, request=request)

        result = []
        for d in ds:
            result.append(Key.from_mongo(d))

        return KeyResponses(
            data=result,
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return handle_error(e, str_time)


@router.post("/", response_model=KeyResponses, responses={
    409: {
        "description": "Resource maybe created. But can't found it.",
    }
})
async def create_key(request: Request, data: KeyInput):
    str_time = time.perf_counter()
    try:
        _id = await key_repository.insert_one(data.model_dump(), request=request)
        d = await key_repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return KeyResponses(
            data=[Key.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.delete("/{id}", response_model=KeyResponses)
async def delete_key(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        d = await key_repository.delete_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return KeyResponses(
            data=None,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail=f"Successfully. [{d}] Resource(s) deleted."
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.put("/{id}", response_model=KeyResponses, responses={
    409: {
        "description": "Resource maybe changed. But can't found it.",
    }
})
async def put_key(
        request: Request,
        id: str,
        data: KeyInput
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        await key_repository.update_one(query={"_id": ObjectId(id)}, update=data.model_dump(),
                                        request=request)
        d = await key_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return KeyResponses(
            data=[Key.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)
