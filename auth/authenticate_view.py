"""
Auth View
"""
import os
import uuid

from dotenv import load_dotenv
from fastapi import Body, HTTPException
from pydantic import EmailStr

import settings
from api.mongo_client import db
from . import router
from .models import pwd_context
from .token_manager import TokenManager, TokenRefreshRequest, TokenResponse

load_dotenv()


@router.post(
    "/authenticate",
    response_model=TokenResponse,
    summary="Get refresh_token and access_token",
    description="This API gives you a cake(access_token) and a baker(refresh_token). "
                f"But don't keep the baker waiting—if you don't put them to work within {settings.REFRESH_TOKEN_TTL} seconds, "
                "they'll walk out on you. No baker, no cake!",
    operation_id="authenticate_user")
async def authenticate(
        account: EmailStr = Body(
            None,
            examples=["<EMAIL>"],
            description="Service Account Username (Must be an email address)"
        ),
        secret: str = Body(
            None,
            examples=["Password_for_human", "API_Key_for_M2M"],
            description="Service Account API Key (Or password for human user)"
        ),
        super_token: str = Body(
            None,
            examples=[uuid.uuid4().hex],
            description="Super Token. You can get it from the environment variable `SUPER_TOKEN`. It only working on DEBUG=True."
        )
):
    tm = TokenManager()
    truck_id = uuid.uuid4().hex

    if super_token:
        if not settings.DEBUG:
            raise HTTPException(status_code=400,
                                detail="Super Token is only working on DEBUG=True. Truck ID: " + truck_id)
        if super_token != settings.SUPER_TOKEN:
            settings.logger.debug(
                f"Truck ID: {truck_id}, Super Token: {super_token}, Super Token from env: {settings.SUPER_TOKEN}")
            raise HTTPException(status_code=400, detail="Super Token is incorrect. Truck ID: " + truck_id)
        else:
            refresh_t, access_t = tm.generate_token(
                account="super_token@role.auth.stayforge.io"
            )
            return TokenResponse(
                access_token=access_t.hex(),
                refresh_token=refresh_t.hex()
            )

    sa: dict = await db.service_account.find_one({"account": account})

    try:
        if pwd_context.verify(secret, sa['secret']):
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
               f"Truck ID: {truck_id}, Debug: {settings.DEBUG}"
    )


@router.post(
    "/refresh_access_token",
    response_model=TokenResponse,
    summary="Refresh an access_token using refresh_token,",
    description=(
            "Think of the `access_token` as the cake, and the Refresh Token as the baker"
            "—basically, the one that keeps the cake coming. "
            "When you've finished your cake, ask your baker to make your bread!"
    ),
    operation_id="refresh_access_token")
async def refresh_access_token(
        body: TokenRefreshRequest
):
    refresh_token = body.refresh_token

    # Super refresh token
    if refresh_token == settings.SUPER_TOKEN:
        tm = TokenManager()
        refresh_t, access_t = tm.generate_token(
            account=os.getenv("SUPER_TOKEN_ACCOUNT", "superuser@role.auth.stayforge.io")
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
