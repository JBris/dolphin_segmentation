class ValidatorBase:

    def __init__(self):
        self.error_message = {} 
        self.message = ""

    def validate(self, data): return data

    def get_error_message(self): 
        error_message = self.error_message
        if self.message != "": error_message["message"] = self.message
        return error_message