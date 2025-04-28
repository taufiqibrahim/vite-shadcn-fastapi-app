from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from src.accounts.models import Account
    from src.projects.models import Project
from src.utils import generate_public_id


class Organization(SQLModel, table=True):
    __tablename__ = "organization"
    __table_args__ = (
        UniqueConstraint("account_id", "name", name=f"uq_{__tablename__}_owner_name"),
    )

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True)
    public_id: str = Field(
        default_factory=lambda: generate_public_id(prefix="org"),
        unique=True,
        index=True,
    )
    name: str = Field(index=True)
    description: Optional[str]

    # Account owner
    account_id: int = Field(
        description="Organization owner account id",
        default=None,
        foreign_key="account.id",
    )
    account: Optional["Account"] = Relationship(back_populates="organizations")

    # List of projects within this organization
    projects: list["Project"] = Relationship(back_populates="organization")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP, onupdate=datetime.now(timezone.utc)),
    )
