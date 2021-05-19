import io
import os
import PIL.Image

from base64 import encodebytes
from pathlib import Path

class Image:
    def check_valid_image(self, path):
        try: 
            with PIL.Image.open(path): return True
        except IOError: return False

    def process_directory(self, path):
        path = Path(path)
        files = path.glob('*')
        file_list = []
        for file in files: 
            classified_file = self.classify_file(str(file), file.name)
            if classified_file: file_list.append(classified_file)
        return file_list

    def classify_file(self, path, name):
        if os.path.isdir(path): return { "type": "dir", "file": path, "name": name }
        image = self.check_valid_image(path)  
        if not image: return False
        return {"type": "image", "file": path, "name": name }
