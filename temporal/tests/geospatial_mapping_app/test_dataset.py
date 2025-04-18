import logging
import os
import shutil
from geospatial_mapping_app.functions import (
    fetch_dataset_from_cloud,
    ogr2ogr_to_postgis,
)
from geospatial_mapping_app.models import DatasetLoadOgr


def test_fetch_dataset_from_cloud_load_postgis(test_dataset):

    # get data from cloud storage
    fetched = fetch_dataset_from_cloud(test_dataset)
    assert isinstance(fetched, DatasetLoadOgr)
    logging.info(f"Fetched into: {fetched.file_path}")

    # use ogr2ogr to load into postgis table
    ogr2ogr_to_postgis(data=fetched)

    # cleanup
    shutil.rmtree(fetched.tmp_dir)
