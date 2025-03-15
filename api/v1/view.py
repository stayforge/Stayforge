"""
Stayforge API v1
Views
"""
import json
import logging
import os
from typing import List, Type

from fastapi import APIRouter
from pydantic import BaseModel

from . import model_classes

router = APIRouter()
logger = logging.getLogger(__name__)


def create_api_routes(_model_name: str, _model_class: Type[BaseModel]):
    """
    Dynamically register API routing
    """

    from .view_templates import _list, _get, _create, _update, _delete

    new_routes = [
        (_list, ["GET"], "/", f"{_model_name}_list"),
        (_get, ["GET"], "/{id}", f"{_model_name}_get"),
        (_create, ["POST"], "/", f"{_model_name}_create"),
        (_update, ["PUT"], "/{id}", f"{_model_name}_update"),
        (_delete, ["DELETE"], "/{id}", f"{_model_name}_delete"),
    ]

    docs = {}
    try:
        docs_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", _model_name, "documents.json"
        )
        with open(docs_path, encoding="utf-8") as f:
            docs = json.load(f)
    except FileNotFoundError:
        logger.warning(
            f"No documentation found for {_model_name}. "
            f"Please create a file called documents.json in the {_model_name} directory."
        )

    for handler_func, methods, endpoint, operation_id in new_routes:
        router.add_api_route(
            path=f"/{_model_name}{endpoint}",
            endpoint=handler_func,
            methods=methods,
            response_model=List[_model_class] if methods == ["GET"] else _model_class,
            tags=[_model_name],
            include_in_schema=True,
            summary=docs.get(operation_id, {}).get('summary', f"{_model_name} {methods[0]}"),
            description=docs.get(operation_id, {}).get('description', f"{methods[0]} operation for {_model_name}"),
            operation_id=operation_id
        )


for model_name, model_class in model_classes.items():
    create_api_routes(model_name, model_class)
