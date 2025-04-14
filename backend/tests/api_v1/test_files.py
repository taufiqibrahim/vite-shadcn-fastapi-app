import os
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

# @pytest.fixture
# def create_app() -> AppCreate:
#     return AppCreate(name="test-app", description="A test app")


def test_upload_file(authorized_headers, client: TestClient):
    """
    Test the POST /api/v1/files/upload endpoint.
    """
    print("test_upload_file 10MB")
    files = {
        "files": ("test.txt", os.urandom(1 * 1024 * 1024), "text/plain"),
    }
    params = {"slug": "default", "actionType": "upload"}
    response = client.post("/api/v1/files/upload", headers=authorized_headers, files=files, params=params)
    print("response", response.status_code, response.json())


#     assert response.status_code == status.HTTP_201_CREATED

#     # get all apps
#     response = client.get("/api/v1/apps/")
#     print(response.status_code)
#     assert response.status_code == status.HTTP_200_OK
