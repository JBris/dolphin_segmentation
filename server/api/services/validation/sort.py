import os

from api.services.content_type import FileFormat
from api.services.validation.validator_base import ValidatorBase 

from enum import Enum, unique

permitted_format =  {
    "file": "task file",
    "format": "csv | json",
    "out": "output/directory"
}

@unique
class FileSortKeys(Enum):
    FILE = "file"
    FORMAT = "format"
    OUT = "out"

class FileSortValidator(ValidatorBase):
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
        for key in FileSortKeys:
            if key.value not in data: return None
        if data["format"] not in [item.value for item in FileFormat]: return None

        del self.error_message["permitted format"]
        self.message = f"Invalid file has been provided: {data['file']}"
        if not os.path.isfile(data["file"]): return None

        return data