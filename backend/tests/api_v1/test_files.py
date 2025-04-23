import os

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from src.core.logging import get_logger

logger = get_logger(__name__)


def test_upload_file(test_account_authorized_headers, client: TestClient):
    """
    Test the POST /api/v1/files/upload endpoint.
    """
    current_path = os.path.abspath(__file__)
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(current_path), "../..", "src", "scripts", "data", "open_energy_sample.json")
    )
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        files = {
            "files": (file_name, f, "text/plain"),
        }
        params = {"slug": "default", "actionType": "upload"}
        response = client.post(
            "/api/v1/files/upload", headers=test_account_authorized_headers, files=files, params=params
        )
    logger.info(f"response status_code={response.status_code} json={response.json()}")
    assert response.status_code == status.HTTP_200_OK
