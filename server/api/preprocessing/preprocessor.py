from api.preprocessing.file_preprocessor import FilePreprocessor
from api.preprocessing.image_preprocessor import ImagePreprocessor

class Preprocessor:

    def preprocess(self, data):
        preprocessed_files = FilePreprocessor().preprocess(data)
        preprocessed_images = ImagePreprocessor().preprocess(preprocessed_files)
        return preprocessed_images