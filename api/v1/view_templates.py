"""
API v1 View Templates
"""
from bson import ObjectId
from fastapi import HTTPException

from api.v1 import repositories
from api.v1.view import model_name, model_class


async def _list():
    repository = repositories[model_name]
    _objects = await repository.find_many({})
    for _object in _objects:
        _object["id"] = str(_object["_id"])
    return _objects


async def _get(id: str):
    repository = repositories[model_name]
    _obj = await repository.find_one({"_id": ObjectId(id)})
    if not _obj:
        raise HTTPException(status_code=404, detail=f"{model_name} not found")
    _obj["id"] = str(_obj["_id"])
    return _obj


async def _create(data: model_class):
    repository = repositories[model_name]
    new_obj = data.model_dump()
    result = await repository.insert_one(new_obj)
    new_obj["id"] = str(result.inserted_id)
    return new_obj


async def _update(id: str, data: model_class):
    repository = repositories[model_name]
    update_result = await repository.update_one(
        {"_id": ObjectId(id)},
        {"$set": data.model_dump(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"{model_name} not found or no update needed")
    updated_obj = await repository.find_one({"_id": ObjectId(id)})
    updated_obj["id"] = str(updated_obj["_id"])
    return updated_obj


async def _delete(id: str):
    repository = repositories[model_name]
    delete_result = await repository.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"{model_name} not found")
    return {"message": "Deleted successfully"},
