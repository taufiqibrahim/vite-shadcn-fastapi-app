import pytest

from geospatial_mapping_app.models import Dataset

# from src.models import Dataset


@pytest.fixture(scope="session")
def test_dataset():
    input_payload = {
        "id": 2,
        "uid": "f639ff5d-bb52-46cc-a92e-c59edec1efd6",
        "account_id": 2,
        "name": "open_energy_sample",
        "description": "open_energy_sample",
        "file_name": "open_energy_sample.json",
        "storage_backend": "minio",
        "storage_uri": "s3://mybucket/uploads/f19c0f80-1611-4198-8cec-73fd5102d794/open_energy_sample.json",
        "status": "uploaded",
        "created_at": "2025-04-17T05:32:18.702Z",
        "updated_at": "2025-04-17T05:32:18.702Z",
    }
    return Dataset(**input_payload)
