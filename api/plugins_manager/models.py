from typing import Optional
from pydantic import BaseModel, Field
import settings
import database

from api.schemas import StayForgeModel
from docs.tools import get_description_md
from repository import MongoRepository

from . import Plugin

collection_name = 'plugin'
logger = settings.getLogger('plugins_loader')

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
        'latest',
        examples=['latest', '1.0.0', '2.1.3'],
        description="The version of the plugin. This helps in tracking updates and ensuring compatibility."
    )
    local_name: Optional[str] = Field(
        None,
        examples=[None, "Demo Plugin"],
        description="Dynamic default value derived from plugin.yaml's name field",
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
        description=get_description_md('plugins_manager', 'PluginsManagerInput', 'permissions.md')
    )


class PluginsManager(PluginsManagerInput, StayForgeModel):
    pass
