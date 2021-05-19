import os
import pandas as pd
from pathlib import Path

class Dataset:

    def process_directory(self, path):
        path = Path(path)
        files = path.glob('*')
        file_list = []
        for file in files: 
            classified_file = self.classify_file(str(file), file.name, file.suffix.lower()[1:])
            if classified_file: file_list.append(classified_file)
        return file_list

    def classify_file(self, path, name, ext):
        if os.path.isdir(path): return { "type": "dir", "file": path, "name": name }
        if not os.path.isfile(path): return False
        if ext == "csv":
            try: 
                pd.read_csv(path)
                return {"type": ext, "file": path, "name": name } 
            except: return False

        if ext == "json":
            try: 
                pd.read_json(path)
                return {"type": ext, "file": path, "name": name } 
            except: return False

        return False
