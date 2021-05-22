import os
import shutil
import tarfile
import zipfile

from decouple import config
from pathlib import Path

from api.services.file_select import FileType
from api.services.validation.file import check_valid_image

#zip | tar | dir | images

def _add_preprocessing_metadata(data, files):
    return {
        "name": data["name"],
        "out": data["out"],
        "type": data["type"],
        "files": files,
        "data": data
    }

def preprocess_archive(data, extracted_path):
    extracted_path_files = os.listdir(extracted_path)
    if len(extracted_path_files) == 1 and os.path.isdir(f"{extracted_path}/{extracted_path_files[0]}"): 
        for file in Path(f"{extracted_path}/{extracted_path_files[0]}").glob("*"): shutil.move(str(file), extracted_path)

    files = []
    for file in Path(extracted_path).glob("*"):
        file = str(file)
        if check_valid_image(file): files.append(file)

    return _add_preprocessing_metadata(data, files)

def preprocess_zip(data):
    with zipfile.ZipFile(data['files'][0], 'r') as f: f.extractall(data['out'])
    return preprocess_archive(data, f"{data['out']}/{Path(data['files'][0]).stem}")

def preprocess_tar(data):
    with tarfile.open(data['files'][0], 'r') as f: f.extractall(data['out'])
    return preprocess_archive(data, f"{data['out']}/{Path(data['files'][0]).stem}")

def preprocess_dir(data):
    full_path = Path(data["files"][0])

    files = []
    for file in full_path.glob("*"):
        file = str(file)
        if check_valid_image(file): files.append(file)

    return _add_preprocessing_metadata(data, files)

def preprocess_images(data):
    files = []
    for file in data["files"]: files.append(file)
    return _add_preprocessing_metadata(data, files)

class FilePreprocessor:
    def preprocess(self, data):
        Path(data['out']).mkdir(parents = True, exist_ok = True)
        if data["type"] == FileType.ZIP.value: return preprocess_zip(data)
        if data["type"] == FileType.TAR.value: return preprocess_tar(data)
        if data["type"] == FileType.DIR.value: return preprocess_dir(data)
        if data["type"] == FileType.IMAGES.value: return preprocess_images(data)
        raise NotImplementedError(f"FilePreprocessor does not support preprocessing of type: {data['type']}")