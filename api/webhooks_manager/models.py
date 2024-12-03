from typing import Dict, Any, Optional

from pydantic import BaseModel, Field

import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

collection_name = 'room_type'

webhooks_manager_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

webhook_logger_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection='logs_webhook',
    client=database.client
)


class WebhooksManagerInput(BaseModel):
    webhook_name: str = Field(
        ...,
        examples=['Your application'],
        description="The Type of WebhooksManager"
    )
    endpoint: str = Field(
        ...,
        examples=['https://youapplocation/webhook/endpoint'],
        description="Description of the room type."
    )
    catch_path: str = Field(
        ...,
        examples=["/api/order/"],
        description="Current price. If you deploy a price controller, this value will be updated automatically."
    )
    catch_method: str = Field(
        ...,
        description="HTTP method to be captured.",
        examples=["POST", "GET"],
    )
    catch_status: int = Field(
        200,
        description="HTTP status to be captured.",
        examples=[200, 400, 500],
    )


class WebhooksManager(WebhooksManagerInput, StayForgeModel):
    pass
