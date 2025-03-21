from typing import Type, Any, Optional

from fastapi import HTTPException
from fastapi_crudrouter_mongodb import CRUDRouter
from pydantic import BaseModel


class FieldBasedCRUDRouter(CRUDRouter):
    """
    A common CRUDRouter subclass,
    using the specified field (identifier_field) as the unique identification key for query,
    update and delete operations.
    """

    def __init__(
            self,
            model: Type[BaseModel],
            db: Any,
            collection_name: str,
            identifier_field: str,
            prefix: str = "",
            tags: Optional[list[str]] = None,
            **kwargs
    ):
        self.identifier_field = identifier_field
        # Save the identifier_field before initializing the parent category
        super().__init__(model, db, collection_name, prefix=prefix, tags=tags, **kwargs)
        # Clear the routes that are automatically generated (because we want to redefine the endpoint based on identifier_field)
        self.routes = []
        self._register_custom_routes()

    def _register_custom_routes(self):
        identifier_field = self.identifier_field
        collection = self.collection_name
        model = self.model

        if not getattr(self, "disable_get_all", False):
            self._add_api_route(
                "/",
                self._get_all(),
                response_model=list[self.model_out],
                dependencies=self.dependencies_get_all,
                methods=["GET"],
                summary=f"Get All {self.model.__name__} from the collection",
                description=f"Get All {self.model.__name__} from the collection",
            )

        @self.get("/{value}", response_model=model, name=f"Get by {identifier_field}")
        async def get_item(value: str):
            doc = await self.db[collection].find_one({identifier_field: value})
            if not doc:
                raise HTTPException(status_code=404, detail=f"{collection} not found")
            return doc

        @self.post("/", response_model=model, name=f"Create {collection}")
        async def create_item(item: model):
            # Check whether there is already a data with the same identifier
            item_dict = item.dict()
            identifier_value = item_dict.get(identifier_field)
            existing = await self.db[collection].find_one({identifier_field: identifier_value})
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"{collection} with {identifier_field}='{identifier_value}' already exists"
                )
            result = await self.db[collection].insert_one(item_dict)
            new_doc = await self.db[collection].find_one({"_id": result.inserted_id})
            return new_doc

        @self.put("/{value}", response_model=model, name=f"Update by {identifier_field}")
        async def update_item(value: str, item: model):
            result = await self.db[collection].update_one(
                {identifier_field: value},
                {"$set": item.dict()}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail=f"{collection} not found or no changes made")
            updated_doc = await self.db[collection].find_one({identifier_field: value})
            return updated_doc

        @self.patch("/{value}", response_model=model, name=f"Patch by {identifier_field}")
        async def patch_item(value: str, partial_data: dict[str, Any]):
            result = await self.db[collection].update_one(
                {identifier_field: value},
                {"$set": partial_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail=f"{collection} not found or no changes made")
            updated_doc = await self.db[collection].find_one({identifier_field: value})
            return updated_doc

        @self.delete("/{value}", response_model=dict, name=f"Delete by {identifier_field}")
        async def delete_item(value: str):
            result = await self.db[collection].delete_one({identifier_field: value})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail=f"{collection} not found")
            return {"detail": f"{collection} deleted"}
