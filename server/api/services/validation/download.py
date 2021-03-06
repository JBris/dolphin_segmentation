from api.services.validation.validator_base import ValidatorBase 

from enum import Enum, unique

permitted_format =  {
    "task": "task name",
    "format": "csv | json",
    "out": "output/path"
}

@unique
class FileDownloadKeys(Enum):
    TASK = "task"
    FORMAT = "format"
    OUT = "out"

class FileDownloadValidator(ValidatorBase):
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
        
        for key in FileDownloadKeys:
            if key.value not in data: return None
            
        return data