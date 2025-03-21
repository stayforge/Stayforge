from datetime import datetime
from typing import List, Optional, Annotated

from bson import ObjectId
from fastapi_crudrouter_mongodb import MongoObjectId
from pydantic import BaseModel, Field

import settings


class Stayforge(BaseModel):
    ver: str = settings.__version__


class StayForgeModel(BaseModel):
    id: Annotated[ObjectId, MongoObjectId] | None = None
    metadata: Optional[dict] = Field(
        None,
        examples=[{
            'picture': '',

        }],
        description="Metadata of this object."
    )
    create_at: Optional[datetime] = Field(
        ...,
        examples=[datetime.now()],
        description="The date of the object being created."
    )
    update_at: Optional[datetime] = Field(
        ...,
        examples=[datetime.now()],
        description="The date of the object being updated."
    )

    def to_mongo(self) -> dict:
        return self.model_dump(exclude_unset=True)

    @classmethod
    def from_mongo(cls, data: dict):
        data['id'] = data.get('_id')
        return cls(**data)


class BaseResponses(BaseModel):
    data: Optional[List[dict]] = None
    detail: str = "Successfully."
    status: int = 200
    used_time: Optional[float] = None
    stayforge: Stayforge = Stayforge()
