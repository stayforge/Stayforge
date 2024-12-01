import time
from typing import List

from bson import ObjectId
from fastapi import *

from .models import *
from ..responses import BaseResponses

router = APIRouter()


class BranchResponses(BaseResponses):
    data: List[Branch]


@router.post("/", response_model=BranchResponses)
async def create_branch(request: Request, data: BranchInput):
    str_time = time.perf_counter()
    _id = await branch_repository.insert_one(data.model_dump(), request=request)
    d = await branch_repository.find_one(query={"_id": ObjectId(_id)})
    if not d:
        return BranchResponses(
            status=404,
            detail="Resource maybe created. But can not access it.",
            used_time=time.perf_counter() - str_time
        )
    return BranchResponses(
        data=[Branch.from_mongo(d)],
        used_time=(time.perf_counter() - str_time) * 1000
    )


@router.get("/", response_model=BranchResponses)
async def get_branch(
        request: Request,
        name: str = Query(default=None),
        address: str = Query(default=None),
        telephone: str = Query(default=None)
):
    str_time = time.perf_counter()
    query = {key: value for key, value in {
        "name": name, "address": address, "telephone": telephone
    }.items() if value}
    ds = await branch_repository.find_many(query=query, request=request)


    result = []
    for d in ds:
        result.append(Branch.from_mongo(d))

    return BranchResponses(
        data=result,
        used_time=(time.perf_counter() - str_time) * 1000
    )


@router.get("/<id>", response_model=BranchResponses)
async def get_branch(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    d = await branch_repository.find_one(query={"_id": ObjectId(id)}, request=request)
    return BranchResponses(
        data=[Branch.from_mongo(d)],
        used_time=(time.perf_counter() - str_time) * 1000
    )
