from decouple import config
from enum import Enum, unique

permitted_format =  {
    "name": "Provide a name for this file selection.",
    "module": "dolphin",
    "task": "segmentation | classification | identification",
    "solver": "umap | triplet_loss",
    "type": "zip | tar | dir | images",
    "files": "[files]",
    "out": "output/directory"
}

optional_parameters =  {
    "autodownload": "1 | 0",
    "cache_duration": config('CACHE_DURATION', default = 86400, cast = str),
}

@unique
class FileSelectKeys(Enum):
    NAME = "name"
    MODULE = "module"
    TASK = "task"
    SOLVER = "solver"
    TYPE = "type"
    FILES = "files"
    OUT = "out"

@unique
class FileModule(Enum):
    DOLPHIN = "dolphin"

@unique
class FileTask(Enum):
    SEGMENTATION = "segmentation"
    CLASSIFICATION = "classification"
    IDENTIFICATION = "identification"

@unique
class FileSolver(Enum):
    UMAP = "umap"
    TRIPLET_LOSS = "triplet_loss"

@unique
class FileType(Enum):
    ZIP = "zip"
    TAR = "tar"
    DIR = "dir"
    IMAGES = "images"

@unique
class FileAutodownload(Enum):
    TRUE = 1
    FALSE = 0
