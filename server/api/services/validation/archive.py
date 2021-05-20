
import os
import tarfile
import zipfile

from enum import Enum, unique

from api.services.validation.validator_base import ValidatorBase 

permitted_format =  {
    "task": "archive | extract",
    "type": "tar | zip",
    "in": "/file/path",
    "out": "/file/path",
}

@unique
class FileArchiveKeys(Enum):
    TASK = "task"
    TYPE = "type"
    IN = "in"
    OUT = "out"

@unique
class FileArchiveTask(Enum):
    ARCHIVE = "archive"
    EXTRACT = "extract"

@unique
class FileArchiveType(Enum):
    TAR = "tar"
    ZIP = "zip"

class FileArchiveValidator(ValidatorBase):
    def __init__(self):
        self.error_message = {
            "error": "1", 
            "message": "Invalid request body format.", 
            "permitted format": permitted_format
        } 

        self.message = ""

    def validate(self, request):
        data = request.get_json()
        if data is None: return None
        for key in FileArchiveKeys:
            if key.value not in data: return None

        if data["task"] not in [item.value for item in FileArchiveTask]: return None
        if data["type"] not in [item.value for item in FileArchiveType]: return None

        del self.error_message["permitted format"]
        self.error_message["message"] = "File does not exist."
        if not os.path.exists(data["in"]): return None
        
        self.error_message["message"] = "Archive does not match the provided type."
        if data["task"] == "extract" and data["type"] == FileArchiveType.ZIP.value:
            if not zipfile.is_zipfile(data["in"]): return None

        if data["task"] == "extract" and data["type"] == FileArchiveType.TAR.value:
            try: 
                if not tarfile.is_tarfile(data["in"]): return None
            except: return None

        return data


