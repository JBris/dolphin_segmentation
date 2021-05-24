import os
import pandas as pd

from api.postprocessing.content_type import FileFormat
from api.services.validation.validator_base import ValidatorBase 

from enum import Enum, unique

permitted_format =  {
    "file": "input/file.",
    "format": "csv | json",
    "method": "umap"
}

@unique
class FileVisualisationKeys(Enum):
    FILE = "file"
    FORMAT = "format"
    METHOD = "method"

class FileVisualisationValidator(ValidatorBase):
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
        
        for key in FileVisualisationKeys:
            if key.value not in data: return None

        return data

class FilePathValidator(ValidatorBase):
    def __init__(self):
        self.error_message = {
            "error": "1", 
            "message": "Provided file is invalid.",
            "file": ""
        } 

        self.message = ""

    def validate(self, data):
        if not os.path.exists(data["file"]):
            self.message = "Provided file path does not exist."
            self.error_message["file"] = data["file"]
            return None

        error_message = f"Provided file does not match format: {data['format']}."
        if data["format"] == FileFormat.CSV.value:
            try: data["data"] = pd.read_csv(data["file"])
            except: 
                self.message = error_message
                self.error_message["file"] = data["file"]
                return None
        
        if data["format"] == FileFormat.JSON.value:
            try: data["data"] = pd.read_json(data["file"], orient='records')
            except: 
                self.message = error_message
                self.error_message["file"] = data["file"]
                return None

        return data

    def get_error_message(self): 
        error_message = self.error_message
        if self.message != "": error_message["message"] = self.message
        return error_message