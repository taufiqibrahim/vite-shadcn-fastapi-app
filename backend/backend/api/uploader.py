import os
from fastapi import APIRouter, Request, Response
from uploadthing_py import (
    UploadThingRequestBody,
    create_uploadthing,
    create_route_handler,
)


router = APIRouter()

upload_router = {
    "videoAndImage": f(
        {
            "image/png": {"max_file_size": "4MB"},
            "image/heic": {"max_file_size": "16MB"},
        }
    )
    # .middleware(middleware)
    # .on_upload_complete(callback)
}
handlers = create_route_handler(
    router=upload_router,
    api_key=os.getenv("UPLOADTHING_SECRET"),
    is_dev=os.getenv("ENVIRONMENT", "development") == "development",
)


@router.get("/uploadthing")
async def ut_get():
    return handlers["GET"]()


@router.post("/uploadthing")
async def ut_post(
    request: Request,
    response: Response,
    body: UploadThingRequestBody,
):
    return await handlers["POST"](
        request=request,
        response=response,
        body=body,
    )
