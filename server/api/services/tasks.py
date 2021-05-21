import os
import json 
from pathlib import Path
from decouple import config

class Tasks:

    def write_file(self, task_id, url, data):
        task_dict = { "id": task_id, "url": url, "status": "created" }
        for key in data: task_dict[key] = data[key]
        task_dir = config('TASK_DIR', default = '/home/app/system/tasks')
        with open(f"{task_dir}/{data['name']}.json", 'w') as f: json.dump(task_dict, f)
        return task_dict

    def process_directory(self, path):
        path = Path(path)
        files = path.glob('*')
        file_list = []
        for file in files: 
            classified_file = self.classify_file(str(file), file.stem, file.suffix.lower()[1:])
            if classified_file: file_list.append(classified_file)
        return file_list

    def classify_file(self, path, name, ext):
        if not os.path.isfile(path): return False
        if ext != "json": return False

        with open(path, 'r') as f: 
            try: data = json.load(f)
            except ValueError: return False

        return {"type": "json", "file": path, "name": name, "status": data.get("status").lower(), "id": data.get("id") } 
