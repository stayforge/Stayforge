import time
from typing import List
from bson import ObjectId
from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class OrderResponses(BaseResponses):
    data: Optional[List[Order]]


@router.get(
    "/order_types",
    description="Call this API or Click `Try it out` and `Execute` to see the order types you can use."
)
async def get_order_types():
    return Order.order_types()


@router.post("/", response_model=OrderResponses,
             description="If the order number is None when creating, it will be automatically created and then returned."
                         "Please record the order number for subsequent operations.",
             responses={
                 409: {
                     "description": "Resource maybe created. But can't found it.",
                 }
             })
async def create_order(request: Request, data: OrderInput):
    str_time = time.perf_counter()
    try:
        data = data.model_dump()
        if not data['num']:
            data['num'] = OrderInput.generate_num()
        _id = await order_repository.insert_one(data, request=request)
        d = await order_repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return OrderResponses(
            data=[Order.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.get("/{id}", response_model=OrderResponses)
async def get_order_by_id(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return OrderResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            ), 400
        d = await order_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return OrderResponses(
            data=[Order.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.get("/num/{num}", response_model=OrderResponses)
async def get_order_by_num(
        request: Request,
        num: str,
        get_all: bool = Query(
            default=False,
            description="Get all orders with the same order number. "
                        "When it's `true`, This time all Orders are returned, "
                        "otherwise `false` **only the latest Order will be returned**."
        )
):
    str_time = time.perf_counter()
    try:
        if get_all:
            query_result = await order_repository.find_many(query={"num": num}, request=request)
            data = [Order.from_mongo(d) for d in query_result]
        else:
            d = await order_repository.find_one(query={"num": num}, request=request)
            if not d:
                return handle_resource_not_found_error(str_time)
            data = [Order.from_mongo(d)]

        return OrderResponses(
            data=data,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail="Returned ALL orders" if get_all else "Returned LATEST order. Set get_all=true to get all orders."
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.delete(
    "/_delete/{id}", response_model=OrderResponses,
    description="**WARING:** Order generally does not need to be deleted. You only need to **create a new one to overwrite it**."
)
async def delete_order(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        d = await order_repository.delete_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return OrderResponses(
            data=None,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail=f"Successfully. [{d}] Resource(s) deleted."
        )
    except Exception as e:
        return handle_error(e, str_time)
