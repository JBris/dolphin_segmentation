from pathlib import Path
import shutil

class Sort:
    def sort(self, data, out, include_metadata = False):
        Path(out).mkdir(parents = True, exist_ok = True)
        for c in data["class"].unique(): Path(f"{out}/{c}").mkdir(parents = True, exist_ok = True)
        
        if include_metadata: copy = shutil.copy2
        else: copy = shutil.copy

        files = {}
        def move_files(row):
            file = row["file"]
            try: files[file] = copy(file, f"{out}/{row['class']}")
            except: files[file] = ""
        data.apply(move_files, axis = 1)

        return files
        