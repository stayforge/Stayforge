from pydantic import BaseModel, Field

import settings
import database
from api.schemas import StayForgeModel
from docs.tools import get_description_md
from repository import MongoRepository

collection_name = 'room_type'

plugins_manager_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

plugin_logger_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection='logs_plugin',
    client=database.client
)


class PluginsManagerInput(BaseModel):
    plugin: str = Field(
        ...,
        examples=[
            "demo-plugin",
            "demo/demo-plugin",
            "https://market.stayforge.io/plugin/demo/demo-plugin"
        ],
        description="The host URL of the plugin. This is used to generate webhook URLs and other plugin-related paths."
    )
    plugin_version: str = Field(
        ...,
        examples=['1.0.0', '2.1.3'],
        description="The version of the plugin. This helps in tracking updates and ensuring compatibility."
    )
    permissions: dict = Field(
        "auto",
        examples=["Auto", "auto", {
            "room": {"_methods": {
                "_post": {
                    "_allow": True,
                    "_webhook": True,
                    "_webhook_path": "/webhook/room_post"
                }
            }}
        }],
        description=get_description_md('plugins_manager', 'PluginsManagerInput', 'permissions.md')
    )



class PluginsManager(PluginsManagerInput, StayForgeModel):
    pass
