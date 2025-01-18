from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class DBResponses(BaseResponses):
    data: TypeVar("T")


def get_collection_name(model_id: str, collection_name: str):
    return f'model_{model_id}.{collection_name}'


@router.post("/find_one/{model_id}/{collection_name}", response_model=DBResponses)
async def find_one(
        request: Request,
        model_id: str = Path(...),
        collection: str = Path(...),
        query: dict = Body(default={}, embed=True),
):
    str_time = time.perf_counter()
    _repository = repository(get_collection_name(model_id, collection))
    try:
        d = await _repository.find_one(query=query, request=request)
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return DBResponses(
            data=[d],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.post("/insert_one/{model_id}/{collection_name}", response_model=DBResponses)
async def insert_one(
        request: Request,
        model_id: str = Path(...),
        collection: str = Path(...),
        document: dict[str, Any] = Body(...),
):
    str_time = time.perf_counter()
    _repository = repository(get_collection_name(model_id, collection))
    try:
        _id = await _repository.insert_one(document, request=request)
        d = await _repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return DBResponses(
            data=[d],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)
