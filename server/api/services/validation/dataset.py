import os
import pandas as pd

from api.postprocessing.content_type import FileFormat
from api.services.validation.validator_base import ValidatorBase 

from enum import Enum, unique

permitted_format =  {
    "path": "/file/path",
    "format": "csv | json",
}

@unique
class FileDatasetKeys(Enum):
    PATH = "path"
    FORMAT = "format"
    
class FileDatasetValidator(ValidatorBase):
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
        for key in FileDatasetKeys:
            if key.value not in data: return None

        if data["format"] not in [item.value for item in FileFormat]: return None

        del self.error_message["permitted format"]
        if not os.path.exists(data["path"]):
            self.message = "Provided file path does not exist."
            self.error_message["file"] = data["path"]
            return None

        if not os.path.isfile(data["path"]):
            self.message = "Provided path is not a file."
            self.error_message["file"] = data["path"]
            return None

        error_message = f"Provided file does not match format: {data['format']}."
        if data["format"] == FileFormat.CSV.value:
            try: data["data"] = pd.read_csv(data["path"]).to_dict(orient="records")
            except: 
                self.message = error_message
                self.error_message["file"] = data["path"]
                return None
        
        if data["format"] == FileFormat.JSON.value:
            try: data["data"] = pd.read_json(data["path"], orient='records').to_dict(orient="records")
            except: 
                self.message = error_message
                self.error_message["file"] = data["path"]
                return None

        return data