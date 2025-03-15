"""
Auth View
"""
from http.client import HTTPException

from fastapi import APIRouter, Body

from .service_account import *
from .token_manager import TokenManager, TokenRefreshRequest

router = APIRouter()


@router.post(
    "/authenticate",
    response_model=TokenResponse,
    summary="Authenticate",
    description="This API gives you a cake(access_token) and a baker(refresh_token). "
                f"But don’t keep the baker waiting—if you don’t put them to work within {settings.REFRESH_TOKEN_TTL} seconds, "
                "they’ll walk out on you. No baker, no cake!",
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
    sa = ServiceAccount(
        account=account,
        secret=secret
    )

    if sa.verify_secret(plain_secret=secret):
        tm = TokenManager(truck_id=truck_id)
        refresh_t, access_t = tm.generate_token(
            account=account
        )

        return TokenResponse(
            access_token=access_t.hex(),
            refresh_token=refresh_t.hex()
        )

    raise HTTPException(
        status_code=401,
        detail=f"Failed to authenticate. \r\n"
               f"Reason: \n"
               f"a. The Service Account does not exist; \n"
               f"b. Verify the information incorrectly; \n"
               f"You need to check whether the Service Account exists by calling '[GET]/auth/service_account/<account>'.\n"
               f"If you deploy Stayforge for the first time, set `DEFAULT_SERVICE_ACCOUNT` and `DEFAULT_SERVICE_ACCOUNT_SECRET` "
               f"through the environment variables.\n"
    )


@router.post(
    "/refresh_access_token",
    response_model=TokenResponse,
    summary="Refresh Access Token",
    description=(
            "Think of the `access_token` as the cake, and the Refresh Token as the baker"
            "—basically, the one that keeps the cake coming. "
            "When you've finished your cake, ask your baker to make your bread!"
    ),
)
async def refresh_access_token(
        body: TokenRefreshRequest
):
    refresh_token = body.refresh_token
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")

    _refresh_token: bytes = bytes.fromhex(refresh_token)

    tm = TokenManager()
    access_token: bytes = tm.generate_access_token(refresh_token=_refresh_token)

    return TokenResponse(
        access_token=access_token.hex(),
        refresh_token=refresh_token
    )
