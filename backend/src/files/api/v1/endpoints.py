from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile
from src.auth.models import Account
from src.auth.services import get_current_active_account_or_400
from src.core.config import settings
from src.files.services import handle_upload_s3, uploadthing_handlers
from uploadthing_py import UploadThingRequestBody

router = APIRouter(prefix="/api/v1/files", tags=["Files"], dependencies=[Depends(get_current_active_account_or_400)])


@router.post("/upload")
async def upload_file(request: Request, response: Response, files: UploadFile = File(...), account: Account = Depends(get_current_active_account_or_400)):
    try:
        if settings.UPLOAD_BACKEND == "uploadthing":
            result = await uploadthing_handlers["POST"](
                request=request,
                response=response,
                body=UploadThingRequestBody(files=files),
            )
            return result
        elif settings.UPLOAD_BACKEND == "s3":
            result = await handle_upload_s3(file=files, account_uid=account.uid)
            return result
        else:
            raise NotImplementedError
        # return JSONResponse(content={"message": "Upload successful", "result": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/", response_model=List[App])
# async def read_apps(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
# ):
#     apps = services.get_apps(db, skip=skip, limit=limit)
#     return apps
