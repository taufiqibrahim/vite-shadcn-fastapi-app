from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta
from src.auth.exceptions import AccountDisabledException, EmailAlreadyExistsException, InvalidLoginCredentialsException
from src.core.config import settings
from src.core.logging import get_logger
from src.auth.models import AccountType
from src.auth.schemas import AccountCreate, AccountCreated, Token, TokenRefresh
from src.auth.services.account import create_account, get_account_by_email
from src.auth.services.jwt import create_access_token, create_refresh_token, get_refresh_token, refresh_access_token
from src.auth.services.security import verify_password

logger = get_logger(__name__)
from src.database.session import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])  #  Define the tag here


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=AccountCreated)
async def signup(account: AccountCreate, db: Session = Depends(get_db)):
    if not account.email or not account.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        account = await create_account(db=db, account=account)
        return account
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsException
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    account = await get_account_by_email(db=db, email=form_data.username.lower())

    if not account or account.account_type != AccountType.USER:
        logger.debug("not account or account.account_type")
        raise InvalidLoginCredentialsException

    if not verify_password(form_data.password, account.hashed_password):
        logger.debug("not verify_password")
        raise InvalidLoginCredentialsException

    if account.disabled:
        logger.debug("account.disabled")
        raise AccountDisabledException

    data = {"sub": account.email.lower(), "id": account.id}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=data, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data=data)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh_token", response_model=TokenRefresh)
async def refresh_token(refresh_token: str = Depends(get_refresh_token)):
    """Endpoint to refresh the JWT access token using the refresh token"""
    try:
        new_access_token = refresh_access_token(refresh_token)
        return TokenRefresh(access_token=new_access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(status_code=302, detail=str(e))
