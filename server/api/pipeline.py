from celery import current_task
from decouple import config

from api.preprocessing.preprocessor import Preprocessor
from api.processing.processor import Processor
from api.postprocessing.postprocessor import PostProcessor

def image_pipeline(data):
    task_name = data["name"]
    out_dir = data["out"]
    task_type = data["task"]  
    if isinstance(data.get("cache_duration"), int): cache_duration = data["cache_duration"]
    else: cache_duration = config('CACHE_DURATION', default = 86400, cast = int)
    
    preprocessed_data = Preprocessor().preprocess(data, current_task)
    processed_data = Processor().process(preprocessed_data, current_task)
    current_task.update_state(state = "PROGRESS", meta = {"step": "Saving data", "step_num": 3, "step_total": 4, "substeps": 0})
    data = PostProcessor().postprocess(processed_data, current_task, task_name, task_type, out_dir, cache_duration)
    return data
