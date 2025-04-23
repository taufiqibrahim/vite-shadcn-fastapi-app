from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from typing import Optional
from src.auth.models import Account, AccountType
from src.auth.schemas import Token
from src.auth.services.account import get_account_by_email
from src.auth.services.jwt import create_access_token
from src.auth.services.security import verify_password
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)
from src.database.session import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])  #  Define the tag here


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.debug(form_data.username, form_data.password)
    account = await get_account_by_email(db=db, email=form_data.username)
    logger.debug(account)

    if not account or account.account_type != AccountType.USER:
        logger.debug("not account or account.account_type")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not verify_password(form_data.password, account.hashed_password):
        logger.debug("not verify_password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if account.disabled:
        logger.debug("account.disabled")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.email, "id": account.id},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")


# @router.get("/api-key", response_model=Token)
# async def get_api_key(
#     current_account: models.Account = Depends(get_current_active_account),
#     db: Session = Depends(get_db),
# ):
#     """
#     Endpoint to generate an API key for the logged-in account.
#     """
#     if current_account.account_type != models.AccountType.SERVICE_ACCOUNT:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="API keys can only be generated for service accounts.",
#         )
#     key = create_api_key(db, current_account.id)
#     return {"access_token": key, "token_type": "api-key"}
