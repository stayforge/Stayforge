"""
Auth View
"""
import os
import uuid

from fastapi import APIRouter, Body, HTTPException
from pydantic import EmailStr

import settings
from settings import SUPERUSER_ACCOUNT_NAME
from .models import pwd_context
from .token_manager import TokenManager, TokenRefreshRequest, TokenResponse
from .. import db

router = APIRouter(prefix="/api/auth")


@router.post(
    "/authenticate",
    response_model=TokenResponse,
    summary="Authenticate, Get refresh_token and access_token",
    description="This API gives you a cake(access_token) and a baker(refresh_token). "
                f"But don’t keep the baker waiting—if you don’t put them to work within {settings.REFRESH_TOKEN_TTL} seconds, "
                "they’ll walk out on you. No baker, no cake!"
)
async def authenticate(
        account: EmailStr = Body(
            ...,
            examples=["<EMAIL>"],
            description="Service Account Username (Must be an email address)"
        ),
        secret: str = Body(
            ...,
            examples=["Password_for_human", "API_Key_for_M2M"],
            description="Service Account API Key (Or password for human user)"
        )
):
    truck_id = uuid.uuid4().hex
    sa = await db.service_account.find_one({"account": account})

    try:
        if pwd_context.verify(secret, sa['secret']):
            tm = TokenManager(truck_id=truck_id)
            refresh_t, access_t = tm.generate_token(
                account=account
            )

            return TokenResponse(
                access_token=access_t.hex(),
                refresh_token=refresh_t.hex()
            )
    except AttributeError as e:
        settings.logger.warning(e, exc_info=True)

    raise HTTPException(
        status_code=401,
        detail=f"Failed to authenticate. \r\n"
               f"Reason: \n"
               f"a. The Service Account does not exist; \n"
               f"b. Verify the information incorrectly; \n"
               f"c. This may also be a database problem."
               f"You need to check whether the Service Account exists by calling '[GET]/auth/service_account/<account>'.\n"
               f"If you deploy Stayforge for the first time, set `DEFAULT_SERVICE_ACCOUNT` and `DEFAULT_SERVICE_ACCOUNT_SECRET` "
               f"through the environment variables.\n"
    )


@router.post(
    "/refresh_access_token",
    response_model=TokenResponse,
    summary="Refresh Tokens, Get an access_token using refresh_token,",
    description=(
            "Think of the `access_token` as the cake, and the Refresh Token as the baker"
            "—basically, the one that keeps the cake coming. "
            "When you've finished your cake, ask your baker to make your bread!"
    )
)
async def refresh_access_token(
        body: TokenRefreshRequest
):
    refresh_token = body.refresh_token

    # Super refresh token
    if refresh_token == os.getenv("SUPER_REFRESH_TOKEN", uuid.uuid4()):
        tm = TokenManager()
        refresh_t, access_t = tm.generate_token(
            account=SUPERUSER_ACCOUNT_NAME
        )

        return TokenResponse(
            access_token=access_t.hex(),
            refresh_token=refresh_t.hex()
        )

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")

    _refresh_token: bytes = bytes.fromhex(refresh_token)

    try:
        tm = TokenManager()
        access_token: bytes = tm.generate_access_token(refresh_token=_refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"{e}"
        )
    return TokenResponse(
        access_token=access_token.hex(),
        refresh_token=refresh_token
    )
