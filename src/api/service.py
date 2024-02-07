import os

from loguru import logger

from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User

from .models import File

from . import schemas, exceptions
from .dao import FileDAO
from .config import ROOT_DIR, UPLOAD_DIR

from ..auth.service import DatabaseManager
from ..utils import get_unique_id


class PathService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.root_path = f"{ROOT_DIR}{UPLOAD_DIR}"

    async def get_folder_path(self, user_id: str) -> str:

        return os.path.join(self.root_path, user_id)

    
    async def get_file_path(self, file_id: int, user_id: str) -> str:
        file = await FileDAO.find_one_or_none(self.db, and_(File.user_id == user_id, File.id == file_id))
        if not file:
            raise exceptions.FileWasNotFound
        
        return file.file_path
    
    @staticmethod
    async def ensure_upload_folder_exists(user_id: str) -> None:
        upload_folder = os.path.join(ROOT_DIR, UPLOAD_DIR)
        user_folder = os.path.join(upload_folder, user_id)

        for folder in [upload_folder, user_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)


import os

class FileCRUD:

    def __init__(self, db: AsyncSession, path_service: PathService):
        self.db = db
        self.path_service = path_service

    async def upload_file(self, token: str, file: UploadFile) -> File:

        try:
            user_id = await self._get_user_id_from_token(token)
            await self.path_service.ensure_upload_folder_exists(user_id)
            
            folder_path = await self.path_service.get_folder_path(user_id)
            file_name, file_extension = os.path.splitext(file.filename)
            original_file_path = os.path.join(folder_path, f"{file_name}{file_extension}")
            file_path = original_file_path

            # Check if the file exists, if so, rename it with an incremental number
            i = 1
            while await self._check_if_file_exists(file_path):
                new_file_name = f"{file_name} ({i}){file_extension}"
                file_path = os.path.join(folder_path, new_file_name)
                i += 1

            logger.info(f"User {user_id} creates file: {file.filename} into {file_path}")

            await self._create_file(file, file_path)
            db_file = await self._upload_file(file_name, file_extension, file_path, user_id, file.size)

            return db_file

        except Exception as e:
            logger.opt(exception=e).critical("Error in upload_file")
            raise e
        
    async def _set_accessed_users(self, user_id: str) -> list:
        
        db_manager = DatabaseManager(self.db)
        user_crud = db_manager.user_crud
        user = await user_crud.get_existing_user(user_id=user_id)
        
        new_accessed_user = [{
            "id": user.id,
            "username": user.username, 
            "email": user.email,
            "type": "author"
        }]
        return new_accessed_user
        
    async def _check_if_file_exists(self, file_path: str) -> bool:
        db_file = await FileDAO.find_one_or_none(self.db, File.file_path == file_path)      
        return db_file

    async def _upload_file(self, file_name, file_extension, file_path, user_id, file_size) -> File:
        
        accessed_users = await self._set_accessed_users(user_id)
        
        db_file = await FileDAO.add(
            self.db,
            schemas.CreateFile(
                id=await get_unique_id(),
                file_name=file_name,
                file_extension=file_extension,
                file_path=file_path,
                file_size=file_size,
                user_id=user_id,
                accessed_users=accessed_users       
            )
        )
        await self.db.commit()
        return db_file
import os

class FileCRUD:

    def __init__(self, db: AsyncSession, path_service: PathService):
        self.db = db
        self.path_service = path_service

    async def upload_file(self, token: str, file: UploadFile) -> File:

        try:
            user_id = await self._get_user_id_from_token(token)
            await self.path_service.ensure_upload_folder_exists(user_id)
            
            folder_path = await self.path_service.get_folder_path(user_id)
            file_name, file_extension = os.path.splitext(file.filename)
            original_file_path = os.path.join(folder_path, f"{file_name}{file_extension}")
            file_path = original_file_path

            i = 1
            while await self._check_if_file_exists(file_path):
                new_file_name = f"{file_name}({i}){file_extension}"
                file_path = os.path.join(folder_path, new_file_name)
                i += 1

            logger.info(f"User {user_id} creates file: {file.filename} into {file_path}")

            await self._create_file(file, file_path)
            db_file = await self._upload_file(file_name, file_extension, file_path, user_id, file.size)

            return db_file

        except Exception as e:
            logger.opt(exception=e).critical("Error in upload_file")
            raise e
        
    async def _set_accessed_users(self, user_id: str) -> list:
        
        db_manager = DatabaseManager(self.db)
        user_crud = db_manager.user_crud
        user = await user_crud.get_existing_user(user_id=user_id)
        
        new_accessed_user = [{
            "id": user.id,
            "username": user.username, 
            "email": user.email,
            "type": "author"
        }]
        return new_accessed_user
        
    async def _check_if_file_exists(self, file_path: str) -> bool:
        db_file = await FileDAO.find_one_or_none(self.db, File.file_path == file_path)      
        return db_file

    async def _upload_file(self, file_extension, file_path, user_id, file_size) -> File:

        accessed_users = await self._set_accessed_users(user_id)

        unique_file_name = os.path.basename(file_path)

        db_file = await FileDAO.add(
            self.db,
            schemas.CreateFile(
                id=await get_unique_id(),
                file_name=unique_file_name,
                file_extension=file_extension,
                file_path=file_path,
                file_size=file_size,
                user_id=user_id,
                accessed_users=accessed_users       
            )
        )
        await self.db.commit()
        return db_file

    async def get_file_metadata(self, token: str, file_id: str) -> File:

        user_id = await self._get_user_id_from_token(token)

        logger.info(f"User {user_id} gets file {file_id}")

        try:
            file = await FileDAO.find_one_or_none(self.db, and_(File.user_id == user_id, File.id == file_id))
            return file

        except Exception as e:
            logger.opt(exception=e).critical("Error in get_file")
            raise
        
    async def get_file(self, token: str, file_id: str) -> File:

        user_id = await self._get_user_id_from_token(token)

        logger.info(f"User {user_id} gets file {file_id}")

        try:
            target_file = await self.path_service.get_file_path(file_id, user_id)
            return target_file

        except Exception as e:
            logger.opt(exception=e).critical("Error in get_file")
            raise

    async def get_user_files(self, token: str, user_id: str, limit: int, offset: int) -> list[File]:
        
        await self._get_user_id_from_token(token)
        
        target_files = await FileDAO.find_all(self.db, File.user_id == user_id, limit=limit, offset=offset)
        
        return target_files
    
    async def get_user_shared_files(self, token: str, user_id: str, limit: int, offset: int) -> list[File]:
        await self._get_user_id_from_token(token)
        
        target_files = await FileDAO.find_all(self.db, limit=limit, offset=offset)
        
        result_files = []
        
        for file_obj in target_files:
            accessed_users = file_obj.accessed_users
            for user_info in accessed_users:
                if user_info.get("id") == user_id and user_info.get("type") == "co-author":
                    result_files.append(file_obj)
                    break
        return result_files
    
    async def update_file(self, token: str, file_id: str, file_in: schemas.UpdateFile) -> File:
        
        user_id = await self._get_user_id_from_token(token) 
        file = await self.get_file_metadata(token, file_id)
                  
        new_abs_path = await self._rename_file(file_id, user_id, file_in, file)
        file_in.file_path = new_abs_path
        file_update = await FileDAO.update(self.db, and_(File.id == file_id, File.user_id == user_id), obj_in=file_in)
        
        await self.db.commit()
        
        return file_update
    
    async def _rename_file(self, file_id: str, user_id: str, file_in: schemas.UpdateFile, file: File) -> str:

        old_file_path = await self.path_service.get_file_path(file_id, user_id)
        folder_path = await self.path_service.get_folder_path(user_id)
        new_abs_path = os.path.join(folder_path, f"{file_in.file_name}.{file.file_extension}")
        os.rename(old_file_path, new_abs_path)
        
        return new_abs_path
    
    async def share_file(self, token: str, file_id: str, user_id: str) -> list:
        
        author_id = await self._get_user_id_from_token(token)
        
        file = await self.get_file_metadata(token, file_id)
        auth_manager = DatabaseManager(self.db)
        user_crud = auth_manager.user_crud
        user = await user_crud.get_existing_user(user_id=user_id)

        current_accessed_users = file.accessed_users or []

        new_accessed_user = {
            "id": user.id,
            "username": user.username, 
            "email": user.email,
            "type": "co-author"
        }
        
        if new_accessed_user not in current_accessed_users:
            current_accessed_users.append(new_accessed_user)
        else:
            current_accessed_users.remove(new_accessed_user)

        obj_in = schemas.UpdateFile(accessed_users=current_accessed_users)
        new_accessed_users = await FileDAO.update(self.db, and_(File.id == file.id, File.user_id == author_id), obj_in=obj_in)

        return new_accessed_users


    async def delete_file(self, token: str, file_id: str) -> str:

        try:
            user_id = await self._get_user_id_from_token(token)
            file_path = await self.path_service.get_file_path(file_id, user_id)           
            logger.info(f"User {user_id} deletes file by file_id: {file_id}")

            if os.path.exists(file_path):
                os.remove(file_path)
                await self._delete_file_db(user_id, file_path)
                return {"Message": f"File {file_path} was deleted by user {user_id} successfully"}
            
            return {"Message": f"File {file_id} does not exist"}        

        except Exception as e:
            logger.opt(exception=e).critical("Error in delete_file")
            raise
        
    async def _delete_file_db(self, user_id: str, file_path: str) -> None:
        
        await FileDAO.delete(self.db, and_(user_id == File.user_id, file_path == File.file_path))
        await self.db.commit()

    async def _get_user_id_from_token(self, token: str):

        db_manager = DatabaseManager(self.db)
        token_service = db_manager.token_crud

        user_id = await token_service.get_access_token_payload(token)
        return user_id

    @staticmethod
    async def _create_file(file: UploadFile, file_path: str) -> None:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)          

class FileManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._path_service = PathService(db)
        self.file_crud = FileCRUD(db, self._path_service)

    async def commit(self):
        await self.db.commit()
