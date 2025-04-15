import os
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select
from src.core.logging import get_logger

logger = get_logger(__name__)


def test_upload_file(authorized_headers, client: TestClient):
    """
    Test the POST /api/v1/files/upload endpoint.
    """
    logger.info("test_upload_file 10MB")
    files = {
        "files": ("test.txt", os.urandom(int(0.1 * 1024 * 1024)), "text/plain"),
    }
    params = {"slug": "default", "actionType": "upload"}
    response = client.post("/api/v1/files/upload", headers=authorized_headers, files=files, params=params)
    logger.info(f"response status_code={response.status_code} json={response.json()}")
    assert response.status_code == status.HTTP_200_OK
