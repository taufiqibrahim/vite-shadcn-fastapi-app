from fastapi import status
from fastapi.testclient import TestClient
from src.geospatial_mapping.models import DatasetCreate, DatasetStatus


def test_create_dataset_process_and_read(
    test_account_authorized_headers, test_account_authorized_account_id, client: TestClient
):
    """
    Test the POST /api/v1/datasets endpoint.
    """
    dataset = DatasetCreate(
        account_id=test_account_authorized_account_id,
        name="test-dataset",
        description="a test dataset",
        status=DatasetStatus.uploaded,
        file_name="test-dataset.txt",
        storage_backend="minio",
        storage_uri="s3://test-bucket/test-dataset.txt",
    )
    response = client.post(
        "/api/v1/geospatial-mapping/datasets",
        headers=test_account_authorized_headers,
        json=dataset.model_dump(mode="json"),
    )
    dataset_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert dataset_response["name"] == "test-dataset"

    # create same name dataset expect to be added (number). For example dataset (1)
    dataset = DatasetCreate(
        account_id=test_account_authorized_account_id,
        name="test-dataset",
        description="a test dataset",
        status=DatasetStatus.uploaded,
        file_name="test-dataset.txt",
        storage_backend="minio",
        storage_uri="s3://test-bucket/test-dataset.txt",
    )
    response = client.post(
        "/api/v1/geospatial-mapping/datasets",
        headers=test_account_authorized_headers,
        json=dataset.model_dump(mode="json"),
    )
    print(response.json())

    # get list of dataset
    response = client.get("/api/v1/geospatial-mapping/datasets", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())


def test_get_dataset_content(test_account_authorized_headers, test_account_authorized_account_id, client: TestClient):
    demo_dataset_uid = "19bea7c2-d17c-47b7-b88a-1fe5133cc1b6"
    response = client.get(
        f"/api/v1/geospatial-mapping/datasets/{demo_dataset_uid}/content", headers=test_account_authorized_headers
    )

    assert response.status_code == 200
