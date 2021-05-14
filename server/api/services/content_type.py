from enum import Enum, unique

@unique
class FileFormat(Enum):
    CSV = "csv"
    JSON = "json"

class ContentType:

    def validate(self, format):
        return format in [item.value for item in FileFormat]

    def convert_df(self, df, format):
        if format == FileFormat.CSV.value: return df.to_csv(index = False, encoding='utf-8')
        if format == FileFormat.JSON.value: return df.to_json(orient="records")
        raise NotImplementedError(f"Format type unsupported: {format}")

    def get_content_type(self, format):
        if format == FileFormat.CSV.value: return f"text/{format}"
        if format == FileFormat.JSON.value: return f"application/{format}"
        raise NotImplementedError(f"Format type unsupported: {format}")
