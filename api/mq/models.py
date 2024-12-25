from typing import Optional

from pydantic import BaseModel, Field

import settings
from api.schemas import StayForgeModel

logger = settings.getLogger('models_loader')


class MQEnqueue(BaseModel):
    message: str = Field(
        None,
        examples=['message'],
        description="The content of the message to be enqueued."
    )


class MQDequeue(BaseModel):
    pass
