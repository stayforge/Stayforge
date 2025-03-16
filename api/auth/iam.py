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

    def checker(account: str):
        user = repository.find_one({"account": account})
        if not user:
            raise HTTPException(status_code=403, detail="User not found")

        # **If the user is admin, then pass directly **
        if user.get("role") == "admin":
            return user

        # **Check whether the user has specified permissions**
        if required_role not in user.get("permissions", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return user

    return checker
