"""OAuth service for social authentication."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import models, schemas
from src.auth.services.jwt import create_access_token


async def get_oauth_account_by_provider_id(
    db: AsyncSession, provider: str, provider_id: str
) -> Optional[models.OAuthAccount]:
    """
    Get an OAuth account by provider and provider ID.

    Args:
        db: Database session
        provider: OAuth provider name
        provider_id: Provider's user ID

    Returns:
        Optional[OAuthAccount]: OAuth account if found, None otherwise
    """
    result = await db.execute(
        select(models.OAuthAccount).where(
            models.OAuthAccount.provider == provider, models.OAuthAccount.provider_id == provider_id
        )
    )
    return result.scalar_one_or_none()


async def create_oauth_account(
    db: AsyncSession, provider: str, provider_id: str, email: str, name: Optional[str] = None
) -> models.OAuthAccount:
    """
    Create a new OAuth account.

    Args:
        db: Database session
        provider: OAuth provider name
        provider_id: Provider's user ID
        email: User email
        name: Optional user name

    Returns:
        OAuthAccount: Created OAuth account
    """
    db_oauth_account = models.OAuthAccount(provider=provider, provider_id=provider_id, email=email, name=name)
    db.add(db_oauth_account)
    await db.commit()
    await db.refresh(db_oauth_account)
    return db_oauth_account


async def get_or_create_oauth_account(
    db: AsyncSession, provider: str, provider_id: str, email: str, name: Optional[str] = None
) -> models.OAuthAccount:
    """
    Get an existing OAuth account or create a new one.

    Args:
        db: Database session
        provider: OAuth provider name
        provider_id: Provider's user ID
        email: User email
        name: Optional user name

    Returns:
        OAuthAccount: Existing or created OAuth account
    """
    oauth_account = await get_oauth_account_by_provider_id(db, provider, provider_id)
    if not oauth_account:
        oauth_account = await create_oauth_account(db, provider, provider_id, email, name)
    return oauth_account


def create_oauth_token(oauth_account: models.OAuthAccount) -> schemas.Token:
    """
    Create an access token for an OAuth account.

    Args:
        oauth_account: OAuth account to create token for

    Returns:
        Token: Access token
    """
    access_token = create_access_token(
        data={"sub": oauth_account.email, "id": oauth_account.id, "provider": oauth_account.provider}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
