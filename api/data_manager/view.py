from typing import List, Optional

from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class DBResponses(BaseResponses):
    data: Optional[List[DB]]


@router.get("/{collection_name}", response_model=DBResponses)
async def get(
        collection: str = Path(...),
        query: DB = Body(default={}, embed=True),
):
    str_time = time.perf_counter()
    _repository = repository(collection)
    try:
        d = await _repository.find_one(query=query)
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return DBResponses(
            data=[DB.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.post("/{collection_name}", response_model=DBResponses)
async def post(
        request: Request,
        collection: str = Path(...),
        document: dict[str, Any] = Body(...),
):
    str_time = time.perf_counter()
    _repository = repository(collection)
    try:
        _id = await _repository.insert_one(document, request=request)
        d = await _repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return DBResponses(
            data=[DB.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)
