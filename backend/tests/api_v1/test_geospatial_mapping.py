from fastapi import status
from fastapi.testclient import TestClient
from src.geospatial_mapping.models import DatasetStatus
from src.geospatial_mapping.schemas import DatasetCreate


def test_create_dataset_process_and_read(authorized_headers, authorized_account_id, client: TestClient):
    """
    Test the POST /api/v1/datasets endpoint.
    """
    dataset = DatasetCreate(
        account_id=authorized_account_id,
        name="test-dataset",
        description="a test dataset",
        status=DatasetStatus.uploaded,
        file_name="test-dataset.txt",
        storage_uri="s3://test-bucket/test-dataset.txt",
    )
    response = client.post("/api/v1/geospatial-mapping/datasets", headers=authorized_headers, json=dataset.model_dump())
    dataset_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert dataset_response["name"] == "test-dataset"

    # create same name dataset expect to be added (number). For example dataset (1)
    dataset = DatasetCreate(
        name="test-dataset",
        description="a test dataset",
        status=DatasetStatus.uploaded,
        file_name="test-dataset.txt",
        storage_uri="s3://test-bucket/test-dataset.txt",
    )
    response = client.post("/api/v1/geospatial-mapping/datasets", headers=authorized_headers, json=dataset.model_dump())
    print(response.json())

    # get list of dataset
    response = client.get("/api/v1/geospatial-mapping/datasets", headers=authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
