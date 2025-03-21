import os
import uuid

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.mongo_client import db
from api.auth.token_manager import TokenManager
from settings import logger

security = HTTPBearer()

_token_manager = TokenManager()


def role(resource_name: str):
    async def checker(
            request: Request,
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        access_token = credentials.credentials

        # Super Token: This is a token used for configuration, mainly used to add Service Account.
        # Defined by environment variable ``. Please delete this configuration after the configuration is completed.
        if access_token == os.getenv("SUPER_TOKEN", uuid.uuid4().hex):
            logger.waring("Super Token used!")
            return True

        method_to_action = {
            "GET": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete"
        }
        action = method_to_action.get(request.method)

        account_name = _token_manager.get_account_name_by_accesstoken(access_token)
        ac_dict: dict = await db.service_account.find_one({"account": account_name})
        if not ac_dict:
            raise HTTPException(status_code=403, detail="User not found")

        if isinstance(ac_dict['role'], list):
            if "superuser" in ac_dict['role']:
                return ac_dict

            for allowed_role in ac_dict['role']:
                allowed_resource, allowed_action = allowed_role.split(":")
                if resource_name == allowed_resource and action == allowed_action:
                    return ac_dict

        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return checker
