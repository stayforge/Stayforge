import os
from typing import Optional, Any, List

from pydantic import BaseModel, PrivateAttr
from starlette.requests import Request
from starlette.responses import Response


def _getenv(key, default=None):
    return os.getenv(f'WEBHOOK_{key}'.upper(), default)


class Fields(BaseModel):
    title: Optional[str] = ''
    name: Optional[str] = ''
    value: Optional[str] = ''
    short: Optional[bool] = True


class Attachments(BaseModel):
    title: str = "Stayforge"
    text: str = "Text"
    color: str = "#36a64f"
    fields: list[dict[str, Any]] = Fields(
        title="k1",
        value="api_factory",
        short=True
    )


class Embeds(BaseModel):
    title: str
    description: str
    url: str
    color: int
    fields: list[dict[str, Any]] = Fields(
        name="k2",
        value="v2"
    )


class Root(BaseModel):
    content: str
    username: str = _getenv("USERNAME")
    avatar_url: str = _getenv("AVATAR_URL", 'https://avatars.githubusercontent.com/u/183347404')
    attachments: List[Attachments]
    embeds: List[Embeds]
    _request: Optional[Request] = PrivateAttr()
    _responses: Optional[Response] = PrivateAttr()
