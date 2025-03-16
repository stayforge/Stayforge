"""
Service Account Model
"""
import secrets
from typing import List, Optional

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, field_validator

import settings
from settings import REFRESH_TOKEN_BYTES, ACCESS_TOKEN_BYTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceAccount(BaseModel):
    account: EmailStr | str = Field(
        ...,
        description="Service Account. It must be **unique** and it is an email address (can be non-real). "
                    "Or a real user email address, usually used when the administrator logs into the panel.",
        example="serviceaccount@role.auth.stayforge.io"
    )
    role: List[str] | None = Field(
        None,
        description="A list of IAM permissions granted to the service account.",
        example=["read", "branch:write", "order:admin"]
    )
    secret: str = Field(
        ...,
        examples=["Password_for_HumanUser", "API_Key_for_M2M"],
        description="`API Key` (For M2M) or `Password` (For human user).",
    )

    # noinspection PyNestedDecorators
    @field_validator("secret", mode="before")
    @classmethod
    def hash_secret(cls, value: str) -> str:
        if value.startswith("$2b$"):
            return value
        return pwd_context.hash(value)

    @property
    def validated_account_name(self) -> EmailStr:
        return EmailStr(self.account)


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
