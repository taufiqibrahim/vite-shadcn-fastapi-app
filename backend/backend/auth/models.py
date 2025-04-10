from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
