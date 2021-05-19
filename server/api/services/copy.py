import os
import shutil

class Copy:
    def copy(self, file, dest, include_metadata = False):
        if include_metadata: copy = shutil.copy2
        else: copy = shutil.copy

        if os.path.isfile(file): 
            try: copy(file, dest)
            except OSError: return False
            
        if os.path.isdir(file):
            try: shutil.copytree(file, dest)
            except OSError: return False 
            
        return True
