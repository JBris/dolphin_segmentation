from api.services.file_download import permitted_format, FileDownloadKeys
from api.services.validation.validator_base import ValidatorBase 

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