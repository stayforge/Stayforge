"""
IAM Permission Checker
"""

from fastapi import HTTPException

from api.auth import repository


def role_checker(required_role: str):
    """
    Dependencies: Check if the user has specified permissions.

    - If the user has 'admin' role, they bypass all permission checks.
    """

    async def checker(account: str):
        user = await repository.find_one({"account": account})
        if not user:
            raise HTTPException(status_code=403, detail="User not found")

        # **If the user is admin, then pass directly **
        if type(user.role) == list:
            if "admin" in user.role:
                return user

            if required_role in user.role:
                return user

        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return checker
