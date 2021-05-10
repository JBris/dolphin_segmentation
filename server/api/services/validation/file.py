import os
import tarfile
import zipfile

from enum import Enum, unique
from pathlib import Path
from PIL import Image

BASE_DIR = "/home/flask/images"

def check_valid_image(path):
    try: 
        with Image.open(path) as test_image: return True
    except IOError: return False

@unique
class FileType(Enum):
    ZIP = "zip"
    TAR = "tar"
    DIR = "dir"
    IMAGES = "images"

class FileValidatorBase:

    def __init__(self):
        self.error_message = {} 
        self.message = ""

    def validate(self, data): return data

    def get_error_message(self): 
        error_message = self.error_message
        if self.message != "": error_message["Message"] = self.message
        return error_message

class FileSelectValidator(FileValidatorBase):
    def __init__(self):
        self.error_message = {
            "Error": "1", 
            "Message": "Invalid request body format.", 
            "Permitted format": {
                "type": "zip | tar | dir | images",
                "files": "[files]"
            }
        } 

        self.message = ""

    def validate(self, request):
        data = request.get_json()
        if data is None: return None
        if "type" not in data or "files" not in data: return None
        if data["type"] not in [item.value for item in FileType]: return None
        
        return data

class FileListValidator(FileValidatorBase):

    def __init__(self):
        self.error_message = {
            "Error": "1", 
            "Message": "Must supply a file list with one or more files.", 
            "Permitted format": {
                "type": "zip | tar | dir | images",
                "files": "[files]"
            }
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

class FilePathValidator(FileValidatorBase):
    def __init__(self):
        self.error_message = {
            "Error": "1", 
            "Message": "One or more supplied files does not exist.",  
            "Files": []
        }

        self.message = ""

    def validate(self, data):
        first_file = data["files"][0]
        full_file_path = f'{BASE_DIR}/{data["files"][0]}'

        def display_error(invalid_file, message):
            self.message = message
            self.error_message["Files"].append(invalid_file)
            return None
            
        if data["type"]  == FileType.ZIP.value or data["type"]  == FileType.TAR.value or data["type"]  == FileType.DIR.value:
            if os.path.exists(full_file_path) is False: return display_error(first_file, "One or more supplied files does not exist.")

        if data["type"]  == FileType.TAR.value:
            tar_message = "Provided tar file is not valid."
            try: 
                if tarfile.is_tarfile(full_file_path) is False: return display_error(first_file, tar_message)
            except: return display_error(first_file, tar_message)

        if data["type"]  == FileType.ZIP.value and zipfile.is_zipfile(full_file_path) is False: 
            return display_error(first_file, "Provided zip file is not valid.")

        if data["type"]  == FileType.DIR.value and os.path.isdir(full_file_path) is False: 
            return display_error(first_file, "Selected directory is not valid.")
        
            #image_path = Path(full_file_path)
            # for image in image_path.glob('*'): 

        if data["type"] == FileType.IMAGES.value:
            error_count = 0
            for image_file in data["files"]:
                full_image_path = f'{BASE_DIR}/{image_file}'
                if os.path.exists(full_image_path): 
                    if check_valid_image(full_image_path): continue
                self.error_message["Files"].append(image_file)
                error_count += 1
            if error_count > 0: 
                self.message = "Invalid image files have been provided."
                return None  

        return data
