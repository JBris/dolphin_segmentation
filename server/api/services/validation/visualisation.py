import os
import pandas as pd

from api.services.content_type import FileFormat
from api.services.file_visualisation import permitted_format, FileVisualisationKeys
from api.services.validation.validator_base import ValidatorBase 

class FileVisualisationValidator(ValidatorBase):
    def __init__(self):
        self.error_message = {
            "Error": "1", 
            "Message": "Invalid request body format.", 
            "Permitted format": permitted_format
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
            "Error": "1", 
            "Message": "Provided file is invalid.",
            "File": ""
        } 

        self.message = ""

    def validate(self, data):
        if not os.path.exists(data["file"]):
            self.message = "Provided file path does not exist."
            self.error_message["File"] = data["file"]
            return None

        error_message = f"Provided file does not match format: {data['format']}."
        if data["format"] == FileFormat.CSV.value:
            try: data["data"] = pd.read_csv(data["file"])
            except: 
                self.message = error_message
                self.error_message["File"] = data["file"]
                return None
        
        if data["format"] == FileFormat.JSON.value:
            try: data["data"] = pd.read_json(data["file"], orient='records')
            except: 
                self.message = error_message
                self.error_message["File"] = data["file"]
                return None

        return data

    def get_error_message(self): 
        error_message = self.error_message
        if self.message != "": error_message["Message"] = self.message
        return error_message