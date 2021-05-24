import os
import pandas as pd

from api.postprocessing.content_type import FileFormat
from api.services.validation.validator_base import ValidatorBase 

from enum import Enum, unique

permitted_format =  {
    "in": "/file/path",
    "in_format": "csv | json",
    "out": "/file/path",
    "out_format": "csv | json"
}

@unique
class FileCopyKeys(Enum):
    IN = "in"
    IN_FORMAT = "in_format"
    OUT = "out"
    OUT_FORMAT = "out_format"
    
class FileCopyValidator(ValidatorBase):
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
        for key in FileCopyKeys:
            if key.value not in data: return None

        if data["in_format"] not in [item.value for item in FileFormat]: return None
        if data["out_format"] not in [item.value for item in FileFormat]: return None

        del self.error_message["permitted format"]
        if not os.path.exists(data["in"]):
            self.message = "Provided file path does not exist."
            self.error_message["file"] = data["in"]
            return None

        if not os.path.isfile(data["in"]):
            self.message = "Provided path is not a file."
            self.error_message["file"] = data["in"]
            return None

        error_message = f"Provided file does not match format: {data['in_format']}."
        if data["in_format"] == FileFormat.CSV.value:
            try: data["data"] = pd.read_csv(data["in"])
            except: 
                self.message = error_message
                self.error_message["file"] = data["in"]
                return None
        
        if data["in_format"] == FileFormat.JSON.value:
            try: data["data"] = pd.read_json(data["in"], orient='records')
            except: 
                self.message = error_message
                self.error_message["file"] = data["in"]
                return None

        return data