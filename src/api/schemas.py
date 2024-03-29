import uuid
from pydantic import BaseModel


class FileBase(BaseModel):
    file_name: str
    file_extension: str
    file_path: str
    file_size: int
    user_id: uuid.UUID
    accessed_users: list = []


class CreateFile(FileBase):
    id: str
    pass    

class UpdateFile(FileBase):
    file_name: str | None = None 
    file_extension: str | None = None 
    file_path: str | None = None
    file_size: int | None = None
    user_id: uuid.UUID | None = None
    accessed_users: list = []

class FileGet(FileBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True
        
class UploadResponse(BaseModel):
    success: bool = False
    message: str = "Failed"
    response: list[FileGet]
    
class MetadataResponse(BaseModel):
    success: bool = False
    message: str = "Failed"
    response: FileGet

class UpdateResponse(BaseModel):
    success: bool = False
    message: str = "Failed"
    response: FileGet

class DeleteResponse(BaseModel):
    success: bool = False
    message: str = "Failed"
