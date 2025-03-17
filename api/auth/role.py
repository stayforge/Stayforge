from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api import db
from api.auth.token_manager import TokenManager

security = HTTPBearer()

_token_manager = TokenManager()


def role(resource_name: str):
    async def checker(
            request: Request,
            credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        access_token = credentials.credentials

        method_to_action = {
            "GET": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete"
        }
        action = method_to_action.get(request.method)

        account_name = _token_manager.get_account_name_by_accesstoken(access_token)
        ac = await db.service_account.find_one({"account": account_name})
        if not ac:
            raise HTTPException(status_code=403, detail="User not found")

        if isinstance(ac.role, list):
            if "admin" in ac.role:
                return ac

            for allowed_role in ac.role:
                allowed_resource, allowed_action = allowed_role.split(":")
                if resource_name == allowed_resource and action == allowed_action:
                    return ac

        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return checker
