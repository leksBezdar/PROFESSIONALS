from pydantic import BaseModel


class FileBase(BaseModel):
    file_name: str
    file_extension: str
    file_path: str
    file_size: int
    user_id: str
    folder_id: int | None = None
    accessed_users: list = []


class CreateFile(FileBase):
    id: str 
    

class UpdateFile(FileBase):
    file_name: str | None = None 
    file_extension: str | None = None 
    file_path: str | None = None
    file_size: int | None = None
    user_id: str | None = None
    folder_id: int | None = None
    accessed_users: list = []



class FolderBase(BaseModel):
    folder_name: str | None = None
    parent_folder_id: int | None = None

class CreateFolder(FolderBase):
    pass
    
class CreateFolderDB(CreateFolder):
    user_id: str
    folder_path: str
    
class UpdateFolder(BaseModel):
    pass
