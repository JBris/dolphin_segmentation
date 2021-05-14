from enum import Enum, unique

from api.visualisation.umap import UMAP

@unique
class VisualisationMethod(Enum):
    UMAP = "umap"

class Visualisation:

    def validate(self, method):
        return method in [item.value for item in VisualisationMethod]

    def visualise(self, method, data):
        if method == VisualisationMethod.UMAP.value: return UMAP().visualise(data)
        raise NotImplementedError(f"Visualisation method not supported: {method}")