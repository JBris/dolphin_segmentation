import os

from api.services.validation.validator_base import ValidatorBase 

class FileDeletionValidator(ValidatorBase):
    def __init__(self):
        self.error_message = {
            "error": "1", 
            "message": "Invalid request body format.", 
            "permitted format": {
                "files": ["file list"]
            }
        } 

        self.message = ""

    def validate(self, request):
        data = request.get_json()
        if data is None: return None
        if "files" not in data: return None
        if isinstance(data["files"], list) is False: return None

        self.message = "Must supply a file list with one or more files."
        if len(data["files"]) == 0: return None
        for selected_file in data["files"]: 
            if isinstance(selected_file, str) is False: return None

        data["files"] = list(set(data["files"]))
        del self.error_message["permitted format"]
        self.error_message["files"] = []
        self.message = "Invalid files have been provided."
        error_count = 0
        for file in data["files"]:
            if not os.path.exists(file):
                error_count += 1
                self.error_message["files"].append(file)

        if error_count > 0: return None
        return data