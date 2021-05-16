from pathlib import Path
import shutil

class Sort:
    def sort(self, data, out, include_metadata = False):
        Path(out).mkdir(parents = True, exist_ok = True)
        if include_metadata: copy = shutil.copy2
        else: copy = shutil.copy

        files = {}
        for file in data["file"]:
            try: files[file] = copy(file, out)
            except: files[file] = ""
        return files
        