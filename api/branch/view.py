from typing import List

from bson import ObjectId
from fastapi import *

from database import client
from .models import *

router = APIRouter()


class BranchRequest(Branch):
    pass


@router.post("/", response_model=Branch)
async def create_branch(request: Request, data: BranchInput):
    _id = await branch_repository.insert_one(data.model_dump(), request=request)
    d = await branch_repository.find_one(query={"_id": ObjectId(_id)})
    if not d:
        raise HTTPException(status_code=404, detail="Resource maybe created. But can not access it.")
    return Branch.from_mongo(d).model_dump()


@router.get("/", response_model=List[Branch])
async def get_branch(
        request: Request,
        name: str = Query(default=None),
        address: str = Query(default=None),
        telephone: str = Query(default=None)
):
    query = {key: value for key, value in {
        "name": name, "address": address, "telephone": telephone
    }.items() if
             value}
    ds = await branch_repository.find_many(query=query, request=request)
    return Branch.from_mongo(ds)


@router.get("/<id>", response_model=Branch)
async def get_branch(
        request: Request,
        id: str
):
    d = await branch_repository.find_one(query={"_id": ObjectId(id)}, request=request)
    return Branch.from_mongo(d).model_dump()
