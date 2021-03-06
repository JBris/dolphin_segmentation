import os
import tarfile
import zipfile

from decouple import config
from pathlib import Path
from PIL import Image

from api.services.file_select import permitted_format, optional_parameters, FileSelectKeys, FileModule, FileTask, FileSolver, FileType
from api.services.validation.validator_base import ValidatorBase 

def check_valid_image(path):
    try: 
        with Image.open(path) as test_image: return True
    except IOError: return False

class FileSelectValidator(ValidatorBase):
    def __init__(self):
        self.error_message = {
            "error": "1", 
            "message": "Invalid request body format.", 
            "permitted format": permitted_format,
            "optional parameters": optional_parameters
        } 

        self.message = ""

    def validate(self, request):
        data = request.get_json()
        if data is None: return None
        
        for key in FileSelectKeys:
            if key.value not in data: return None

        if data["module"] not in [item.value for item in FileModule]: return None
        if data["task"] not in [item.value for item in FileTask]: return None
        if data["solver"] not in [item.value for item in FileSolver]: return None
        if data["type"] not in [item.value for item in FileType]: return None
        if data["out"] == "": return None
        
        return data

class FileListValidator(ValidatorBase):

    def __init__(self):
        self.error_message = {
            "error": "1", 
            "message": "Must supply a file list with one or more files.", 
            "permitted format": permitted_format,
            "optional parameters": optional_parameters
        }
        
        self.message = ""

    def validate(self, data):
        if isinstance(data["files"], list) is False: return None
        if len(data["files"]) == 0: return None
        
        for selected_file in data["files"]: 
            if isinstance(selected_file, str) is False: return None

        if data["type"]  == FileType.ZIP.value or data["type"]  == FileType.TAR.value or data["type"]  == FileType.DIR.value:
            if len(data["files"]) > 1:
                self.message = "You may only process one archive file or directory at a time."
                return None

        data["files"] = list(set(data["files"]))
        return data

class FilePathValidator(ValidatorBase):
    def __init__(self):
        self.error_message = {
            "error": "1", 
            "message": "One or more supplied files does not exist.",  
            "files": []
        }

        self.message = ""

    def validate(self, data):
        first_file = data["files"][0]

        def display_error(invalid_file, message):
            self.message = message
            self.error_message["files"].append(invalid_file)
            return None
            
        if data["type"]  == FileType.ZIP.value or data["type"]  == FileType.TAR.value or data["type"]  == FileType.DIR.value:
            if os.path.exists(data["files"][0]) is False: return display_error(first_file, "One or more supplied files does not exist.")

        if data["type"]  == FileType.TAR.value:
            tar_message = "Provided tar file is not valid."
            try: 
                if tarfile.is_tarfile(data["files"][0]) is False: return display_error(first_file, tar_message)
            except: return display_error(first_file, tar_message)

        if data["type"]  == FileType.ZIP.value and zipfile.is_zipfile(data["files"][0]) is False: 
            return display_error(first_file, "Provided zip file is not valid.")

        if data["type"]  == FileType.DIR.value and os.path.isdir(data["files"][0]) is False: 
            return display_error(first_file, "Selected directory is not valid.")

        if data["type"] == FileType.IMAGES.value:
            error_count = 0
            for image_file in data["files"]:
                if os.path.exists(image_file): 
                    if check_valid_image(image_file): continue
                self.error_message["files"].append(image_file)
                error_count += 1
            if error_count > 0: 
                self.message = "Invalid image files have been provided."
                return None  

        return data
