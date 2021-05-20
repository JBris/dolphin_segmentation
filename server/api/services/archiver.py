import os
import shutil
import tarfile
import zipfile
import subprocess
from pathlib import Path

from api.services.validation.archive import FileArchiveTask, FileArchiveType

class Archiver:
    def process(self, task, type, inFile, out):
        if task == FileArchiveTask.ARCHIVE.value: return self.archive(type, inFile, out)
        if task == FileArchiveTask.EXTRACT.value: return self.extract(type, inFile, out)
        raise NotImplementedError(f"Task has not been implemented: {task}")

    def archive(self, type, inFile, out):
        Path(Path(out).parent).mkdir(parents = True, exist_ok = True)

        if type == FileArchiveType.TAR.value:
            os.chdir(Path(inFile).parent)
            subprocess.call(['tar', '-czf', out, Path(inFile).name])
            return True            

        if type == FileArchiveType.ZIP.value: 
            os.chdir(Path(inFile).parent)
            if os.path.isdir(inFile): shutil.make_archive(out, 'zip', Path(inFile).name)
            if os.path.isfile(inFile): 
                with zipfile.ZipFile(out, 'w') as z: z.write(Path(inFile).name) 
            return True

        raise NotImplementedError(f"Type has not been implemented: {type}")

    def extract(self, type, inFile, out):
        Path(Path(out).parent).mkdir(parents = True, exist_ok = True)

        if type == FileArchiveType.TAR.value:
            with tarfile.open(inFile, 'r') as f: 
                f.extractall(out)
                return True

        if type == FileArchiveType.ZIP.value: 
            with zipfile.ZipFile(inFile, 'r') as f: 
                f.extractall(out)
                return True

        raise NotImplementedError(f"Type has not been implemented: {type}")