"""
mq
"""
from typing import *

from fastapi import *

from mq import MessageQueue
from .models import *
from ..schemas import BaseResponses

router = APIRouter()


class MessageQueueResponses(BaseResponses):
    data: Optional[List[MQDequeue]]


@router.post("/{stream}")
async def enqueue(stream: str, data: MQEnqueue, ttl: int = -1):
    try:
        mq = MessageQueue(stream_name=stream)
        mq.enqueue(data.message)
        return {"last_message": data.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sized/{stream}")
async def sized(stream: str):
    try:
        mq = MessageQueue(stream_name=stream)
        return {"sized": mq.size()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages/{stream}")
async def messages(stream: str):
    try:
        mq = MessageQueue(stream_name=stream)
        return {"messages": mq.messages()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/streams")
async def streams():
    try:
        mq = MessageQueue()
        return {"streams": mq.streams()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
