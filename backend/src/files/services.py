import os
import uuid

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from minio import Minio, S3Error
from uploadthing_py import create_route_handler, create_uploadthing

from src.core.config import minio_settings, secret_settings, settings
from src.core.logging import get_logger

logger = get_logger(__name__)


f = create_uploadthing()

uploadthing_upload_router = {
    "default": f({})
    # .middleware(lambda req: {"user_id": req.headers["x-user-id"]})
    .on_upload_complete(lambda file, metadata: print(f"Upload complete for {metadata['user_id']}")),
    "videoAndImage": f(
        {
            "image/png": {"max_file_size": "4MB"},
            "image/heic": {"max_file_size": "16MB"},
        }
    )
    # .middleware(lambda req: {"user_id": req.headers["x-user-id"]})
    .on_upload_complete(lambda file, metadata: print(f"Upload complete for {metadata['user_id']}")),
}

uploadthing_handlers = create_route_handler(
    router=uploadthing_upload_router,
    api_key=secret_settings.UPLOAD_BACKEND_UPLOADTHING_SECRET,
    is_dev=os.getenv("ENVIRONMENT", "development") == "development",
)


s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION"))

BUCKET_NAME = settings.UPLOAD_BACKEND_S3_BUCKET_NAME

transfer_config = TransferConfig(
    multipart_chunksize=8 * 1024 * 1024,  # 8MB
    multipart_threshold=8 * 1024 * 1024,  # 8MB
)


async def handle_upload_s3(file: UploadFile, account_uid: str):
    logger.debug("Using S3 upload handler")

    try:
        await file.seek(0)

        s3_key = f"uploads/{account_uid}/{file.filename}"

        s3.upload_fileobj(Fileobj=file.file, Bucket=BUCKET_NAME, Key=s3_key, Config=transfer_config)

        return {
            "name": file.filename,
            "url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}",
            "storage_backend": "s3",
            "storage_uri": f"s3://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}",
        }

    except NoCredentialsError:
        raise Exception("AWS credentials not found")
    except Exception as e:
        raise Exception(f"S3 upload failed: {str(e)}")


# MinIO Config
MINIO_ENDPOINT = minio_settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = minio_settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = minio_settings.MINIO_SECRET_KEY
MINIO_UPLOAD_BUCKET_NAME = "uploads"
MINIO_SECURE = minio_settings.MINIO_SECURE

# MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE,
)


async def handle_upload_minio(file: UploadFile, uid: uuid.UUID = None):
    logger.debug("Using MinIO upload handler")

    try:
        # Make sure the bucket exists
        found = minio_client.bucket_exists(MINIO_UPLOAD_BUCKET_NAME)
        if not found:
            minio_client.make_bucket(MINIO_UPLOAD_BUCKET_NAME)

        _, extension = os.path.splitext(file.filename)

        if not uid:
            uid = uuid.uuid4()

        object_name = f"{uid}{extension}"

        # Upload the file
        await file.seek(0)
        minio_client.put_object(
            bucket_name=MINIO_UPLOAD_BUCKET_NAME,
            object_name=object_name,
            data=file.file,
            length=-1,  # unknown length (streaming)
            part_size=10 * 1024 * 1024,  # 10 MB chunks
        )

        return {
            "name": file.filename,
            "uid": uid,
            "storage_backend": "minio",
            "storage_uri": f"s3://{MINIO_UPLOAD_BUCKET_NAME}/{object_name}",
        }

    except S3Error as e:
        logger.error(f"MinIO SDK error: {str(e)}")
        raise Exception(f"MinIO upload failed: {str(e)}")
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        raise Exception(f"Upload failed: {str(e)}")
