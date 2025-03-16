"""
IAM Permission Checker
"""

from fastapi import HTTPException, Header

from api.auth import repository
from api.auth.token_manager import TokenManager

_token_manager = TokenManager()


def role_checker(required_role: str):
    """
    Dependencies: Check if the ac has specified permissions.

    - If the ac has 'admin' role, they bypass all permission checks.
    """

    async def checker(access_token: str = Header(None, alias="Authorization")):
        print(access_token)

        ac = await repository.find_one({"account": ""})
        if not ac:
            raise HTTPException(status_code=403, detail="User not found")

        # **If the ac is admin, then pass directly **
        if type(ac.role) == list:
            if "admin" in ac.role:
                return ac

            if required_role in ac.role:
                return ac

        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return checker
