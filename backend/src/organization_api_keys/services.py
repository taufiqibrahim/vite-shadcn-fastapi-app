import secrets

from sqlmodel import Session

from src.organization_api_keys.models import APIKey


def create_api_key(
    db: Session, account_id: int, level: int = 1, api_key: str = None
) -> str:
    if not api_key or api_key is None:
        key = secrets.token_urlsafe(32)
    else:
        key = api_key
    db_api_key = APIKey(key=key, account_id=account_id, level=level)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return key
