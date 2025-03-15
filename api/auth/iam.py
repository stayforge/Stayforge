"""
IAM Permission Checker
"""
from fastapi import HTTPException

from api.auth import sa_repository


def check_permission(required_permission: str):
    """
    Dependencies: Check if the user has specified permissions.

    - If the user has 'admin' role, they bypass all permission checks.
    """

    def permission_checker(email: str):
        user = sa_repository.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=403, detail="User not found")

        # **If the user is admin, then pass directly **
        if user.get("role") == "admin":
            return user

        # **Check whether the user has specified permissions**
        if required_permission not in user.get("permissions", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return user

    return permission_checker
