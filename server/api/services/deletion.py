import os
import shutil

class Deletion:
    def delete(self, file):
        if os.path.isfile(file): 
            try: os.remove(file)
            except OSError: return False
            
        if os.path.isdir(file):
            try: shutil.rmtree(file)
            except OSError: return False 
            
        return True

    def delete_multiple(self, files):
        deletions = {}
        for file in files:
            if self.delete(file): deletions[file] = 1
            else: deletions[file] = 0
        return deletions
