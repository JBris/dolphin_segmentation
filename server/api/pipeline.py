from celery import current_task
from decouple import config
from flask import current_app

from api.preprocessing.preprocessor import Preprocessor
from api.processing.processor import Processor
from api.services.content_type import ContentType
from api.services.serializer import Serializer

def image_pipeline(data):
    task_name = data["name"]
    out_dir = data["out"]

    if isinstance(data.get("cache_duration"), int): cache_duration = data["cache_duration"]
    else: cache_duration = config('CACHE_DURATION', default = 86400, cast = int)
    
    preprocessed_data = Preprocessor().preprocess(data, current_task)
    processed_data = Processor().process(preprocessed_data, current_task)
    current_task.update_state(state = "PROGRESS", meta = {"step": "Saving data", "step_num": 3, "step_total": 4, "substeps": 0})
    ContentType().write_df(processed_data, task_name, "csv", out_dir)
    serialised_data = Serializer().serialize(processed_data) 
    current_task.update_state(state = "PROGRESS", meta = {"step": "Caching data", "step_num": 4, "step_total": 4, "substeps": 0})
    current_app.config["CACHE"].set(f"processed_images_{task_name}", serialised_data, ex = cache_duration)
    return True