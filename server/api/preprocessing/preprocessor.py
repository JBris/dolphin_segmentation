from api.preprocessing.file_preprocessor import FilePreprocessor

class Preprocessor:

    def preprocess(self, data):
        preprocessed_file = FilePreprocessor().preprocess(data)
        return preprocessed_file