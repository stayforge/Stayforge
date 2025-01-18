"""
mq
"""
from pydantic import BaseModel, Field
import settings

logger = settings.getLogger('models_loader')


class MQEnqueue(BaseModel):
    message: str = Field(
        None,
        examples=['message'],
        description="The content of the message to be enqueued."
    )


class MQDequeue(BaseModel):
    pass
