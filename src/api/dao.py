from .models import File, Folder, DeletedFile
from .schemas import CreateFile, CreateFolder, UpdateFile, UpdateFolder, CreateDeletedFile, UpdateDeletedFile

from ..dao import BaseDAO


class FileDAO(BaseDAO[File, CreateFile, UpdateFile]):
    model = File


class FolderDAO(BaseDAO[Folder, CreateFolder, UpdateFolder]):
    model = Folder

