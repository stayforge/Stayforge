"""
Token Generator & Manager
"""
import hashlib
import secrets
import uuid
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr, BaseModel, Field

import settings
from api import RedisClient
from settings import ACCESS_TOKEN_BYTES, REFRESH_TOKEN_BYTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenManager:
    @staticmethod
    def sha256(b: bytes) -> str:
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
        self.refresh_token_hash = self.sha256(self.refresh_token)

        # Save Redis and set TTL
        self.refresh_token_client.set(self.refresh_token_hash, account)
        self.refresh_token_client.expire(self.refresh_token_hash, self.refresh_token_ttl)

        return self.refresh_token, self.generate_access_token(self.refresh_token)

    def generate_access_token(self, refresh_token: bytes) -> bytes:
        """Generate an access token based on a valid refresh token"""
        self.refresh_token = refresh_token
        self.refresh_token_hash = self.sha256(self.refresh_token)

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
        self.access_token_hash = self.sha256(self.access_token)

        # Storage access_token and set TTL
        self.access_token_client.set(self.access_token_hash, f"{self.refresh_token}|{account}")
        self.access_token_client.expire(self.access_token_hash, self.access_token_ttl)

        return self.access_token

    def get_account_name_by_accesstoken(self, access_token: bytes | str) -> str:
        """Get the account name associated with the given access token."""
        if isinstance(access_token, str):
            access_token = bytes.fromhex(access_token)

        self.access_token_hash = self.sha256(access_token)
        token_data = self.access_token_client.get(self.access_token_hash)

        if token_data is None:
            raise ValueError("Invalid access token")

        # Extract the account name from the stored token data
        refresh_token, account = token_data.decode().split('|')
        return account


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        examples=[secrets.token_bytes(REFRESH_TOKEN_BYTES).hex()],
        description=f"Your baker, A {REFRESH_TOKEN_BYTES}-byte random byte stream turned into a fancy hex string."
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
