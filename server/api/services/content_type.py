from decouple import config
from enum import Enum, unique
from pathlib import Path

@unique
class FileFormat(Enum):
    CSV = "csv"
    JSON = "json"

DATASET_DIR = config('DATASET_DIR', default = '/home/app/datasets')

class ContentType:

    def validate(self, format):
        return format in [item.value for item in FileFormat]

    def convert_df(self, df, format):
        if format == FileFormat.CSV.value: return df.to_csv(index = False, encoding='utf-8')
        if format == FileFormat.JSON.value: return df.to_json(orient="records")
        raise NotImplementedError(f"Format type unsupported: {format}")

    def write_df(self, df, task, format, path):
        path = f"{DATASET_DIR}/{path}"
        Path(path).mkdir(parents = True, exist_ok = True)
        out = f"{path}/{task}.{format}"
        if format == FileFormat.CSV.value: return df.to_csv(out, index = False, encoding='utf-8'), out
        if format == FileFormat.JSON.value: return df.to_json(out, orient="records"), out
        raise NotImplementedError(f"Format type unsupported: {format}")

    def get_content_type(self, format):
        if format == FileFormat.CSV.value: return f"text/{format}"
        if format == FileFormat.JSON.value: return f"application/{format}"
        raise NotImplementedError(f"Format type unsupported: {format}")
