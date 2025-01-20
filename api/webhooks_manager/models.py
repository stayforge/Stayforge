from typing import Literal, Optional, List

from pydantic import BaseModel, Field, HttpUrl

import database
import settings
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
    retry_status_code: Optional[List[str]] = Field(
        ['!200', '300', '401-409'],
        description="Retry status code. Syntax: !200 (all except 200), 400 (single status), 500-599 (status range). "
                    "When the other server returns the specified retry_status_code, retry will be triggered.",
        examples=[['!200', '400', '!300-399', '500-599']]
    ),
    retry_times: Optional[int | str] = Field(
        'always',
        description="Retry times(int or 'always')",
        examples=[10, 'always']
    )


class WebhooksManager(WebhooksManagerInput, StayForgeModel):
    pass
