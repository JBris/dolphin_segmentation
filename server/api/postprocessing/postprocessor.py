from flask import current_app

from api.postprocessing.content_type import ContentType
from api.postprocessing.serializer import Serializer
from api.services.file_select import FileTask

class PostProcessor:
    def postprocess(self, processed_data, current_task, task_name, task_type, out_dir, cache_duration):
        if task_type == FileTask.SEGMENTATION.value: return processed_data
        
        ContentType().write_df(processed_data, task_name, "csv", out_dir)
        serialised_data = Serializer().serialize(processed_data) 
        current_task.update_state(state = "PROGRESS", meta = {"step": "Caching data", "step_num": 4, "step_total": 4, "substeps": 0})
        current_app.config["CACHE"].set(f"processed_images_{task_name}", serialised_data, ex = cache_duration)
        return serialised_data
