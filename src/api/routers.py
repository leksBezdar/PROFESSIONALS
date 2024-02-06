from fastapi import APIRouter, Depends, UploadFile, File

from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session

from .service import FileManager
from . import schemas

router = APIRouter(prefix="/files")


@router.post("/upload_file")
async def upload_file(
    token: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session)
    ):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud
    
    return await file_crud.upload_file(token=token, file=file)


@router.get("/get_file_metadata/{file_id}")
async def get_file_metadata(
    file_id: str,
    token: str,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud
    
    target_file = await file_crud.get_file_metadata(token=token, file_id=file_id)
    
    return target_file


@router.get("/download_file/{file_id}")
async def download_file(
    file_id: str,
    token: str,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud
    
    target_file = await file_crud.get_file(token=token, file_id=file_id)
    
    return FileResponse(target_file)


@router.patch("/share")
async def share_file(
    token: str, 
    file_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud

    return await file_crud.share_file(token, file_id, user_id)


@router.get("/get_user_files/{user_id}")
async def get_user_files(
    token: str, 
    user_id: str,
    limit: int = 100, 
    offset: int = 0,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud

    return await file_crud.get_user_files(token, user_id, limit=limit, offset=offset)


@router.get("/get_user_shared_files/{user_id}")
async def get_user_shared_files(
    token: str, 
    user_id: str,
    limit: int = 100, 
    offset: int = 0,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud

    return await file_crud.get_user_shared_files(token, user_id, limit=limit, offset=offset)


@router.patch("/update_file/{file_id}")
async def update_file(
    token: str, 
    file_id: str,
    file_in: schemas.UpdateFile,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud

    return await file_crud.update_file(token=token, file_in=file_in, file_id=file_id)
    
    
@router.delete("/delete_file/{file_id}")
async def delete_file(
    token: str,
    file_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    
    file_manager = FileManager(db)
    file_crud = file_manager.file_crud
    
    return await file_crud.delete_file(token, file_id)