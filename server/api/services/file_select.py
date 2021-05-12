from enum import Enum, unique

permitted_format =  {
    "name": "Provide a name for this file selection.",
    "module": "dolphin",
    "task": "identification | classification",
    "solver": "umap | triplet_loss",
    "type": "zip | tar | dir | images",
    "files": "[files]"
}

@unique
class FileSelectKeys(Enum):
    NAME = "name"
    MODULE = "module"
    TASK = "task"
    SOLVER = "solver"
    TYPE = "type"
    FILES = "files"

@unique
class FileModule(Enum):
    DOLPHIN = "dolphin"

@unique
class FileTask(Enum):
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
