from fastapi import HTTPException


class FileAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="File already exists")
        
class FileWasNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Not found")