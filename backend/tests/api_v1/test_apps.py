import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.apps.schemas import AppCreate


@pytest.fixture
def create_app() -> AppCreate:
    return AppCreate(name="test-app", description="A test app")


def test_create_and_list_app(test_account_authorized_headers, client: TestClient, create_app: AppCreate):
    """
    Test the POST /api/v1/apps/ endpoint.
    """
    print("new_app:", create_app)

    response = client.post(
        "/api/v1/apps/", json=create_app.model_dump(mode="json"), headers=test_account_authorized_headers
    )
    print("response", response.json())
    assert response.status_code == status.HTTP_201_CREATED

    # get all apps
    response = client.get("/api/v1/apps/", headers=test_account_authorized_headers)
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
