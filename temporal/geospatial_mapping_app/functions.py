import subprocess
import logging
import os
import shutil
import tempfile
import httpx
from minio import Minio
from urllib.parse import urlparse
from sqlalchemy import URL, create_engine, inspect, select, text
from sqlalchemy.orm import Session

logging.basicConfig(
    level=logging.INFO,  # or logging.DEBUG for more verbosity
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from base import minio_settings, postgis_settings, settings
from geospatial_mapping_app.models import Dataset, DatasetLoadOgr

mc = Minio(
    minio_settings.MINIO_ENDPOINT,
    access_key=minio_settings.MINIO_ACCESS_KEY,
    secret_key=minio_settings.MINIO_SECRET_KEY,
    secure=minio_settings.MINIO_SECURE,
)

MINIO_BUCKET_NAME = os.getenv("GEOSPATIAL_MAPPING_APP_MINIO_BUCKET_NAME", "uploads")


def notify_backend(dataset_uid: str, dataset_update: dict):
    logging.info(f"dataset_uid={dataset_uid} dataset_update={dataset_update}")
    api_url = f"{settings.BACKEND_API_BASE_URL}/api/v1/geospatial-mapping/datasets/{dataset_uid}"
    headers = {
        "X-API-Key": settings.BACKEND_API_KEY,
        "Content-Type": "application/json",
    }
    logging.info(f"api_url={api_url} headers={headers}")

    try:
        response = httpx.put(api_url, json=dataset_update, headers=headers)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logging.error(f"Failed to notify FastAPI: {e}")


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
        "-lco", "GEOMETRY_NAME=geom",
    ]

    # Run the command
    try:
        subprocess.run(ogr2ogr_command, check=True)
        logging.info("Data loaded successfully into PostGIS.")
        return data
    except subprocess.CalledProcessError as e:
        logging.error(f"ogr2ogr failed (code {e.returncode})")
        raise Exception
    finally:
        shutil.rmtree(data.tmp_dir)


def update_dataset_metadata(data: DatasetLoadOgr):
    pg_table = "u_" + str(data.uid).replace("-", "_")
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=postgis_settings.POSTGIS_USER,
        password=postgis_settings.POSTGIS_PASSWORD,
        host=postgis_settings.POSTGIS_HOST,
        port=postgis_settings.POSTGIS_PORT,
        database=postgis_settings.POSTGIS_DB,
    )
    engine = create_engine(db_url)
    with Session(engine) as session:
        
        logging.info("Getting bounding box...")
        query = text(f"""
            SELECT
                JSON_BUILD_OBJECT(
                    'xmin', ST_XMin(extent),
                    'ymin', ST_YMin(extent),
                    'xmax', ST_XMax(extent),
                    'ymax', ST_YMax(extent)
                ) AS bbox
            FROM (
                SELECT ST_Extent(geom) AS extent
                FROM {pg_table}
            ) AS sub
        """)
        result = session.execute(query).mappings().first()
        bbox = result["bbox"]

        logging.info("Getting primary key column...")
        inspector = inspect(engine)
        schema = 'public'
        pk_info = inspector.get_pk_constraint(pg_table, schema)
        pk_columns = pk_info.get("constrained_columns", [])
        primary_key_column = pk_columns[0]

        return {
            "status": "ready",
            "bbox": bbox,
            "primary_key_column": primary_key_column,
        }
