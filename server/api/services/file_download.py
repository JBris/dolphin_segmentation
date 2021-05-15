from enum import Enum, unique

permitted_format =  {
    "task": "task name",
    "format": "csv | json",
    "out": "output/path"
}

@unique
class FileDownloadKeys(Enum):
    TASK = "task"
    FORMAT = "format"
    OUT = "out"
