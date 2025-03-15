"""
Token Generator & Manager
"""
import hashlib
import os
import secrets
import uuid
from typing import Optional

from pydantic import EmailStr

import settings
from api import RedisClient
from settings import ACCESS_TOKEN_BYTES, REFRESH_TOKEN_BYTES


class TokenManager:
    @staticmethod
    def _sha256(b: bytes) -> str:
        return hashlib.sha256(b).hexdigest()

    def __init__(self, truck_id: str = uuid.uuid4()):
        self.truck_id = truck_id
        self.refresh_token_ttl = settings.REFRESH_TOKEN_TTL
        self.access_token_ttl = settings.ACCESS_TOKEN_TTL

        self.access_token: Optional[bytes] = None
        self.refresh_token: Optional[bytes] = None

        self.access_token_hash: Optional[str] = None
        self.refresh_token_hash: Optional[str] = None

        self.access_token_client = RedisClient(path='stayforge_accesstoken').client
        self.refresh_token_client = RedisClient(path='stayforge_refreshtoken').client

    """Generates tokens"""

    def generate_token(self, account: EmailStr | str) -> tuple[bytes, bytes]:
        """Generate refresh_token and store in Redis"""
        self.refresh_token = secrets.token_bytes(REFRESH_TOKEN_BYTES)
        self.refresh_token_hash = self._sha256(self.refresh_token)

        # Save Redis and set TTL
        self.refresh_token_client.set(self.refresh_token_hash, account)
        self.refresh_token_client.expire(self.refresh_token_hash, self.refresh_token_ttl)

        return self.refresh_token, self.generate_access_token(self.refresh_token)

    def generate_access_token(self, refresh_token: bytes) -> bytes:
        """Generate an access token based on a valid refresh token"""
        self.refresh_token = refresh_token
        self.refresh_token_hash = self._sha256(self.refresh_token)

        # Get account information from Redis
        account = self.refresh_token_client.get(self.refresh_token_hash)

        if account is not None:
            account = account.decode()
        else:
            raise ValueError("Invalid refresh token")

        # **Refresh refresh_token TTL**
        self.refresh_token_client.expire(self.refresh_token_hash, self.refresh_token_ttl)

        # Generate a new access_token
        self.access_token = secrets.token_bytes(ACCESS_TOKEN_BYTES)
        self.access_token_hash = self._sha256(self.access_token)

        # Storage access_token and set TTL
        self.access_token_client.set(self.access_token_hash, f"{self.refresh_token}|{account}")
        self.access_token_client.expire(self.access_token_hash, self.access_token_ttl)

        return self.access_token


def super_refresh_token() -> str:
    """
    Super refresh_token

    This refresh_token is assigned by `SUPER_REFRESH_TOKEN` in the environment variable.
    Each time it is used, it checks whether the ServiceAccount has been created.
    When the ServiceAccount has been created and has the AIM permission of `admin`,
    it will be disabled (the function will return None to prevent abuse).
    This feature is used when creating a root account when first configuring Stayforge.

    :return: The `SUPER_REFRESH_TOKEN` value from environment variables, or `None` if not set.
    :rtype: str or None
    """
    _super_refresh_token = os.getenv("SUPER_REFRESH_TOKEN", uuid.uuid4())
    return _super_refresh_token
