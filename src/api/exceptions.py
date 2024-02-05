from fastapi import HTTPException


class FolderAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="Folder already exists")
        
class FileAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="File already exists")
        
class FolderWasNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Not found")
        
class FileWasNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Not found")