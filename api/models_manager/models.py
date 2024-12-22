from typing import Optional
from pydantic import BaseModel, Field
import settings
import database

from api.schemas import StayForgeModel
from docs.tools import get_description_md
from repository import MongoRepository

from . import Model

collection_name = 'model'
logger = settings.getLogger('models_loader')

models_manager_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

model_logger_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection='logs_model',
    client=database.client
)


class ModelsManagerInput(BaseModel):
    model: str = Field(
        ...,
        examples=[
            "demo-model",
            "demo/demo-model",
            "https://market.stayforge.io/model/demo/demo-model"
        ],
        description="The host URL of the model. This is used to generate webhook URLs and other model-related paths."
    )
    model_version: str = Field(
        'latest',
        examples=['latest', '1.0.0', '2.1.3'],
        description="The version of the model. This helps in tracking updates and ensuring compatibility."
    )
    local_name: Optional[str] = Field(
        None,
        examples=[None, "Demo Model"],
        description="Dynamic default value derived from model.yaml's name field",
    )
    permissions: Optional[dict] = Field(
        None,
        examples=[None, {
            "room": {"_methods": {
                "_post": {
                    "_allow": True,
                    "_webhook": True,
                    "_webhook_path": "/webhook/room_post"
                }
            }}
        }],
        description=get_description_md('models_manager', 'ModelsManagerInput', 'permissions.md')
    )


class ModelsManager(ModelsManagerInput, StayForgeModel):
    pass
