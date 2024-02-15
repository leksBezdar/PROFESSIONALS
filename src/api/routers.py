from fastapi import APIRouter, UploadFile, File

from fastapi.responses import FileResponse

from .service import FileManager
from . import schemas

router = APIRouter(prefix="/files")


@router.post("/upload_file")
async def upload_files(
    token: str,
    files: list[UploadFile] = File(...)
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud
    
    return schemas.UploadResponse(
        success=True,
        message="Success",
        response=await file_crud.upload_file(token=token, files=files))

@router.get("/get_file_metadata/{file_id}")
async def get_file_metadata(
    file_id: str,
    token: str,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud
    
    target_file = await file_crud.get_file_metadata(token=token, file_id=file_id)
    
    return schemas.MetadataResponse(success=True, message="File_metadata", response=target_file)


@router.get("/download_file/{file_id}")
async def download_file(
    file_id: str,
    token: str,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud
    
    target_file = await file_crud.get_file_metadata(token=token, file_id=file_id)
    
    return FileResponse(target_file.file_path, filename=target_file.file_name, media_type='application/octet-stream')


@router.patch("/share")
async def share_file(
    token: str, 
    file_id: str,
    user_id: str,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud

    return await file_crud.share_file(token, file_id, user_id)


@router.get("/get_user_files/{user_id}")
async def get_user_files(
    token: str, 
    user_id: str,
    limit: int = 100, 
    offset: int = 0,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud

    return await file_crud.get_user_files(token, user_id, limit=limit, offset=offset)


@router.get("/get_user_shared_files/{user_id}")
async def get_user_shared_files(
    token: str, 
    user_id: str,
    limit: int = 100, 
    offset: int = 0,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud

    return await file_crud.get_user_shared_files(token, user_id, limit=limit, offset=offset)


@router.patch("/update_file/{file_id}")
async def update_file(
    token: str, 
    file_id: str,
    file_in: schemas.UpdateFile,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud

    return schemas.UpdateResponse(
        success=True,
        message="Renamed",
        response=await file_crud.update_file(token=token, file_in=file_in, file_id=file_id)
    )
    
@router.delete("/delete_file/{file_id}")
async def delete_file(
    token: str,
    file_id: str,
):
    
    file_manager = FileManager()
    file_crud = file_manager.file_crud
    
    await file_crud.delete_file(token, file_id)
    
    return schemas.DeleteResponse(success=True, message="File was deleted successfuly")