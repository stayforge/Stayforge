from typing import *
from warnings import catch_warnings

from bson import ObjectId
from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class WebhooksManagerResponses(BaseResponses):
    data: Optional[List[WebhooksManager]]


@router.get("/", response_model=WebhooksManagerResponses,
    operation_id="list_webhook_profiles")
async def get_webhooks_profile(
        request: Request,

        webhook_name: str = Query(
            None,
            description="A friendly name you can remember."
        ),
        endpoint: str = Query(
            None,
            regex="^(https?|http|https)://[a-zA-Z,\\*\\s]+/?$",
            description="The URL endpoint where the webhook is to be sent, e.g., `https://youapplocation/webhook/endpoint`."
        ),
        catch_path: str = Query(
            None,
            regex="^(/[^/ ]*)+/?$",
            description="This refers to the API within Stayforage, the path part of its URL e.g., `/api/order/`."
        ),
        catch_method: str = Query(
            None,
            description="Only configured HTTP methods (e.g., `POST`) that the request will capture."
        ),
        catch_status: int = Query(
            None,
            description="Only configured HTTP status code (e.g., `200`) that the request will capture."
        ),
):
    str_time = time.perf_counter()

    try:
        query = {key: value for key, value in {
            "webhook_name": webhook_name, "endpoint": endpoint,
            "catch_path": catch_path, "catch_method": catch_method, "catch_status": catch_status
        }.items() if value}
        ds = await webhooks_manager_repository.find_many(query=query, request=request)

        result = []
        for d in ds:
            result.append(WebhooksManager.from_mongo(d))

        return WebhooksManagerResponses(
            data=result,
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return handle_error(e, str_time)


@router.get("/{id}", response_model=WebhooksManagerResponses,
    operation_id="get_webhook_profile")
async def get_webhook_profile_by_id(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return WebhooksManagerResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        d = await webhooks_manager_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return WebhooksManagerResponses(
            data=[WebhooksManager.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.post("/", response_model=WebhooksManagerResponses, responses={
    409: {
        "description": "Resource maybe created. But can't found it.",
    }
}, operation_id="create_webhook_profile")
async def create_webhooks_profile(request: Request, data: WebhooksManagerInput):
    str_time = time.perf_counter()
    try:
        _id = await webhooks_manager_repository.insert_one(data.model_dump(), request=request)
        d = await webhooks_manager_repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return WebhooksManagerResponses(
            data=[WebhooksManager.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.delete("/{id}", response_model=WebhooksManagerResponses,
    operation_id="delete_webhook_profile")
async def delete_webhooks_profile(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        d = await webhooks_manager_repository.delete_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return WebhooksManagerResponses(
            data=None,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail=f"Successfully. [{d}] Resource(s) deleted."
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.put("/{id}", response_model=WebhooksManagerResponses, responses={
    409: {
        "description": "Resource maybe changed. But can't found it.",
    }
}, operation_id="update_webhook_profile")
async def put_webhooks_profile(
        request: Request,
        id: str,
        data: WebhooksManagerInput
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        await webhooks_manager_repository.update_one(query={"_id": ObjectId(id)}, update=data.model_dump(),
                                                     request=request)
        d = await webhooks_manager_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return WebhooksManagerResponses(
            data=[WebhooksManager.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)
