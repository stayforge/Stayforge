"""
Service Account Model
"""
import secrets
import uuid
from typing import List, Optional

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

import settings
from api.schemas import StayForgeModel
from settings import REFRESH_TOKEN_BYTES, ACCESS_TOKEN_BYTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceAccountBase(BaseModel):
    account: EmailStr | str = Field(
        ...,
        description="Service Account. It must be an email address (it can be non-real). "
                    "Or a real user email address, usually used when the administrator logs into the panel.",
        example="serviceaccount@iam.auth.stayforge.io"
    )
    secret: str = Field(
        ...,
        examples=[f"{"Password_for_HumanUser", "API_Key_for_M2M"}"],
        description="`API Key` (For M2M) or `Password` (For human user).",
    )

    @property
    def validated_account_name(self) -> EmailStr:
        return EmailStr(self.account)

    def verify_secret(self, plain_secret: str) -> bool:
        """Verify password or API Key"""
        return pwd_context.verify(plain_secret, self.secret)

    @classmethod
    def hash_secret(cls, secret: str) -> str:
        """Hash password or API Key"""
        return pwd_context.hash(secret)

    @classmethod
    def generate_secret_key(cls) -> str:
        """Generate a secure API Key"""
        return str(uuid.uuid4())


class ServiceAccount(ServiceAccountBase, StayForgeModel):
    iam: List[str] = Field(
        ...,
        examples=[
            [
                "read",
                "branch:write",
                "order:admin"
            ]
        ],
    )

class TokenResponse(BaseModel):
    access_token: Optional[str] = Field(
        ...,
        examples=[secrets.token_bytes(ACCESS_TOKEN_BYTES).hex()],
        description=f"A {ACCESS_TOKEN_BYTES}-byte random byte stream turned into a fancy hex string as your Access Token."
                    f"You can use this token to access the service, but its validity period is only `{settings.ACCESS_TOKEN_TTL}` seconds. When it expires, please refresh it."
    )
    refresh_token: Optional[str] = Field(
        ...,
        examples=[secrets.token_bytes(REFRESH_TOKEN_BYTES).hex()],
        description=f"A {REFRESH_TOKEN_BYTES}-byte random byte stream turned into a fancy hex string as your Refresh Token."
                    f"This token is specially used to generate a new Access Token, "
                    f"and its validity period is `{settings.REFRESH_TOKEN_TTL}` seconds. "
                    f"If you use the Refresh Token within the validity period, it will restart the timing. "
                    f"Otherwise, it will disappear after expiration."
    )
