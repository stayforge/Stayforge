"""
Service Account Models
"""
from typing import List, Annotated

from bson import ObjectId
from fastapi_crudrouter_mongodb import MongoObjectId
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, field_validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceAccount(BaseModel):
    id: Annotated[ObjectId, MongoObjectId] | None = None
    account: str = Field(
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

    def to_mongo(self) -> dict:
        return self.model_dump(exclude_unset=True)

    @classmethod
    def from_mongo(cls, data: dict) -> 'ServiceAccount':
        data['id'] = data.get('_id')
        return cls(**data)
