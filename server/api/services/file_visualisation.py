from enum import Enum, unique

permitted_format =  {
    "file": "input/file.",
    "format": "csv | json",
    "method": "umap"
}

@unique
class FileVisualisationKeys(Enum):
    FILE = "file"
    FORMAT = "format"
    METHOD = "method"
