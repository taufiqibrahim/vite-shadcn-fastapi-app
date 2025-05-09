"""add initial tables

Revision ID: 001
Revises:
Create Date: 2025-04-17 18:44:46.363820

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uid", sa.Uuid(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("account_type", sa.Enum("USER", "SERVICE_ACCOUNT", name="accounttype"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_account_email"), "account", ["email"], unique=True)
    op.create_index(op.f("ix_account_id"), "account", ["id"], unique=False)
    op.create_index(op.f("ix_account_uid"), "account", ["uid"], unique=True)
    op.create_table(
        "app",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uid", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_app_id"), "app", ["id"], unique=False)
    op.create_index(op.f("ix_app_uid"), "app", ["uid"], unique=True)
    op.create_table(
        "api_key",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("uid", sa.Uuid(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_api_key_id"), "api_key", ["id"], unique=False)
    op.create_index(op.f("ix_api_key_key"), "api_key", ["key"], unique=True)
    op.create_index(op.f("ix_api_key_uid"), "api_key", ["uid"], unique=True)
    op.create_table(
        "user_profile",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uid", sa.Uuid(), nullable=False),
        sa.Column("full_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_profile_id"), "user_profile", ["id"], unique=False)
    op.create_index(op.f("ix_user_profile_uid"), "user_profile", ["uid"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_profile_uid"), table_name="user_profile")
    op.drop_index(op.f("ix_user_profile_id"), table_name="user_profile")
    op.drop_table("user_profile")
    op.drop_index(op.f("ix_api_key_uid"), table_name="api_key")
    op.drop_index(op.f("ix_api_key_key"), table_name="api_key")
    op.drop_index(op.f("ix_api_key_id"), table_name="api_key")
    op.drop_table("api_key")
    op.drop_index(op.f("ix_app_uid"), table_name="app")
    op.drop_index(op.f("ix_app_id"), table_name="app")
    op.drop_table("app")
    op.drop_index(op.f("ix_account_uid"), table_name="account")
    op.drop_index(op.f("ix_account_id"), table_name="account")
    op.drop_index(op.f("ix_account_email"), table_name="account")
    op.drop_table("account")
    # ### end Alembic commands ###
