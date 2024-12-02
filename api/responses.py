from typing import List, Optional

from pydantic import BaseModel

import settings


class Stayforge(BaseModel):
    ver: str = settings.__version__


class BaseResponses(BaseModel):
    data: Optional[List[dict]] = None
    detail: str = "Successfully."
    status: int = 200
    used_time: Optional[float] = None
    stayforge: Stayforge = Stayforge()
