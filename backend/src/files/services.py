import os
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from src.core.config import settings, secret_settings
from src.core.logging import get_logger

logger = get_logger(__name__)
from uploadthing_py import create_route_handler, create_uploadthing


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
    api_key=secret_settings.UPLOADTHING_SECRET,
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

        return {"url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"}

    except NoCredentialsError:
        raise Exception("AWS credentials not found")
    except Exception as e:
        raise Exception(f"S3 upload failed: {str(e)}")
