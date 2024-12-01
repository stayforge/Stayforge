from bson import ObjectId
from fastapi import *

from database import client
from .models import *

router = APIRouter()


class BranchRequest(Branch):
    pass


@router.post("/", response_model=Branch)
async def create_branch(branch_data: BranchInput, request: Request):
    branch_id = await branch_repository.insert_one(branch_data.model_dump(), request=request)
    branch = await branch_repository.find_one(query={"_id": ObjectId(branch_id)})
    if not branch:
        raise HTTPException(status_code=404, detail="Resource maybe created. But can not access it.")
    return Branch.from_mongo(branch)
