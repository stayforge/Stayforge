from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

import settings


class Stayforge(BaseModel):
    ver: str = settings.__version__


class StayForgeModel(BaseModel):
    id: Optional[str]
    create_at: Optional[datetime]
    update_at: Optional[datetime]

    @classmethod
    def from_mongo(cls, document: dict | list):
        if document:
            document["id"] = str(document["_id"])
            del document["_id"]
            if document is None:
                raise ValueError("Document is None")
        return cls(**document)



class BaseResponses(BaseModel):
    data: Optional[List[dict]] = None
    detail: str = "Successfully."
    status: int = 200
    used_time: Optional[float] = None
    stayforge: Stayforge = Stayforge()
