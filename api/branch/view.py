import time
from typing import List
from bson import ObjectId
from fastapi import *

from settings import logger
from .models import *
from ..responses import BaseResponses

router = APIRouter()


class BranchResponses(BaseResponses):
    data: Optional[List[Branch]]


@router.post("/", response_model=BranchResponses)
async def create_branch(request: Request, data: BranchInput):
    str_time = time.perf_counter()
    try:
        _id = await branch_repository.insert_one(data.model_dump(), request=request)
        d = await branch_repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return BranchResponses(
                status=404,
                detail="Resource maybe created. But can't found it.",
                used_time=time.perf_counter() - str_time,
                data=None
            )
        return BranchResponses(
            data=[Branch.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return BranchResponses(
            status=500,
            detail=str(e),
            used_time=time.perf_counter() - str_time,
            data=None
        )


@router.get("/", response_model=BranchResponses)
async def get_branches(
        request: Request,
        name: str = Query(default=None),
        address: str = Query(default=None),
        telephone: str = Query(default=None)
):
    str_time = time.perf_counter()
    try:
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
    except Exception as e:
        logger.error(e, exc_info=True)
        return BranchResponses(
            status=500,
            detail="An error occurred while retrieving branches.",
            used_time=time.perf_counter() - str_time,
            data=None
        )


@router.get("/<id>", response_model=BranchResponses)
async def get_branch(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return BranchResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        d = await branch_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return BranchResponses(
                status=404,
                detail="Resource not found",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )

        return BranchResponses(
            data=[Branch.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return BranchResponses(
            status=500,
            detail=str(e),
            used_time=time.perf_counter() - str_time,
            data=None
        )


@router.delete("/<id>", response_model=BranchResponses)
async def delete_branch(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return BranchResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        d = await branch_repository.delete_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return BranchResponses(
                status=404,
                detail="Resource not found",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )

        return BranchResponses(
            data=None,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail=f"Successfully. [{d}] Resource(s) deleted."
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return BranchResponses(
            status=500,
            detail=str(e),
            used_time=time.perf_counter() - str_time,
            data=None
        )


@router.put("/{id}", response_model=BranchResponses, responses={
    404: {
        "description": "Resource maybe changed. But can't found it.",
    }
})
async def put_branch(
        request: Request,
        id: str,
        data: BranchInput
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return BranchResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        await branch_repository.update_one(query={"_id": ObjectId(id)}, update=data.model_dump(),
                                           request=request)
        d = await branch_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return BranchResponses(
                status=404,
                detail="Resource maybe changed. But can't found it.",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        return BranchResponses(
            data=[Branch.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return BranchResponses(
            status=500,
            detail=str(e),
            used_time=time.perf_counter() - str_time,
            data=None
        )
