import httpx
from fastapi import HTTPException, Path, APIRouter
from pydantic import BaseModel

from settings import ETCD_ENDPOINT

etcd_router = APIRouter()


class KeyValueRequest(BaseModel):
    key: str
    value: str = None

def get_key(model:str, key:str):
    return f"{model}__{key}"

@etcd_router.post("/{model}/etcd/put")
async def put_data(request: KeyValueRequest, model: str = Path(...)):
    full_key = get_key(model, request.key)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ETCD_ENDPOINT}/v3/kv/put",
            json={"key": full_key, "value": request.value}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"message": "Data stored successfully", "key": full_key, "value": request.value}


# Read
@etcd_router.get("/{model}/etcd/get/{key}")
async def get_data(key: str, model: str = Path(...)):
    full_key = get_key(model, key)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ETCD_ENDPOINT}/v3/kv/range",
            json={"key": full_key}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    data = response.json()
    if not data.get("kvs"):
        raise HTTPException(status_code=404, detail="Key not found")
    value = data["kvs"][0]["value"]
    return {"key": full_key, "value": value}


# Delete
@etcd_router.delete("/{model}/etcd/delete/{key}")
async def delete_data(key: str, model: str = Path(...)):
    full_key = get_key(model, key)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ETCD_ENDPOINT}/v3/kv/deleterange",
            json={"key": full_key}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"message": "Key deleted successfully", "key": full_key}
