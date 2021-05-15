from api.preprocessing.file_preprocessor import FilePreprocessor
from api.preprocessing.image_preprocessor import ImagePreprocessor

class Preprocessor:

    def preprocess(self, data, current_task):
        current_task.update_state(state = "PROGRESS", meta = {"step": "Preprocessing images", "step_num": 1, "step_total": 4, "substeps": 0})
        preprocessed_files = FilePreprocessor().preprocess(data)
        preprocessed_images = ImagePreprocessor().preprocess(preprocessed_files)
        return preprocessed_images