import subprocess
import logging
import os
import shutil
import tempfile
from minio import Minio
from urllib.parse import urlparse

from base import minio_settings, postgis_settings
from geospatial_mapping_app.models import Dataset, DatasetLoadOgr

mc = Minio(
    minio_settings.MINIO_ENDPOINT,
    access_key=minio_settings.MINIO_ACCESS_KEY,
    secret_key=minio_settings.MINIO_SECRET_KEY,
    secure=minio_settings.MINIO_SECURE,
)

MINIO_BUCKET_NAME = os.getenv("GEOSPATIAL_MAPPING_APP_MINIO_BUCKET_NAME", "mybucket")


def fetch_dataset_from_cloud(dataset: Dataset) -> DatasetLoadOgr:

    if dataset.storage_backend == "minio":
        logging.info("minio handler")
        tmp_dir = tempfile.mkdtemp()

        parsed = urlparse(dataset.storage_uri)
        bucket_name = parsed.netloc
        object_name = parsed.path.lstrip("/")
        tmp_file_path = os.path.join(tmp_dir, dataset.file_name)
        mc.fget_object(bucket_name, object_name, tmp_file_path)

        return DatasetLoadOgr(
            uid=dataset.uid, tmp_dir=tmp_dir, tmp_file_path=tmp_file_path
        )
    elif dataset.storage_backend == "s3":
        logging.info("s3 handler")
        raise NotImplementedError
    else:
        raise NotImplementedError


def ogr2ogr_to_postgis(data: DatasetLoadOgr) -> DatasetLoadOgr:

    pg_table = "u_" + str(data.uid).replace("-", "_")

    # Build the ogr2ogr command
    ogr2ogr_command = [
        "ogr2ogr",
        "-f",
        "PostgreSQL",
        f"PG:host={postgis_settings.POSTGIS_HOST} port={postgis_settings.POSTGIS_PORT} user={postgis_settings.POSTGIS_USER} dbname={postgis_settings.POSTGIS_DB} password={postgis_settings.POSTGIS_PASSWORD}",
        data.tmp_file_path,
        "-nln",
        pg_table,
        "-a_srs",
        "EPSG:4326",
        "-overwrite",
    ]

    # Run the command
    try:
        subprocess.run(ogr2ogr_command, check=True)
        logging.info("Data loaded successfully into PostGIS.")
        return data
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {str(e)}")
    finally:
        shutil.rmtree(data.tmp_dir)
