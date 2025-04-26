from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: EmailStr
    id: int
    jti: str
    exp: Optional[int] = None


class TokenRefresh(BaseModel):
    access_token: str
    token_type: str
