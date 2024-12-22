from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl
import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

# Collection Names
WEBHOOK_COLLECTION = 'webhook'
LOGS_COLLECTION = 'logs_webhook'

# MongoDB Repositories
webhooks_manager_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=WEBHOOK_COLLECTION,
    client=database.client
)

webhook_logger_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=LOGS_COLLECTION,
    client=database.client
)

# Pydantic Models
class WebhooksManagerInput(BaseModel):
    webhook_name: str = Field(
        ...,
        examples=['Your application'],
        description="The name of the webhook configuration."
    )
    endpoint: HttpUrl = Field(
        ...,
        examples=['https://yourapplication/webhook/endpoint'],
        description="The URL where webhook events will be sent."
    )
    catch_path: str = Field(
        ...,
        examples=["/api/order/"],
        description="The path to monitor for webhook events."
    )
    catch_method: Literal["POST", "GET", "PUT", "DELETE"] = Field(
        ...,
        description="HTTP method to be captured.",
        examples=["POST", "GET"],
    )
    catch_status: Optional[int] = Field(
        200,
        description="HTTP status to be captured. Defaults to 200.",
        examples=[200, 400, 500],
    )

class WebhooksManager(WebhooksManagerInput, StayForgeModel):
    pass