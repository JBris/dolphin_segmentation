import numpy as np
import pandas as pd

from api.processing.models.clustering.hdbscan import HDBSCAN
from api.processing.models.dim_reduction.umap import UMAP
from api.services.file_select import FileSolver

def create_processed_df(embeddings, cluster, data):
    return pd.DataFrame(
        index = np.arange(
            cluster.labels_.shape[0] 
        ), 
        data = {
            'index' : np.arange(cluster.labels_.shape[0]),
            'name': data["preprocessed_names"],
            'x': embeddings[:, 0],
            'y': embeddings[:, 1],
            'file': data["files"],
            'class': cluster.labels_,
            'probability': cluster.probabilities_,
            'outlier': [ 1 if item == -1 else 0 for item in cluster.labels_ ]
        }
    )

class Processor:
    def process(self, data):
        if data["data"]["solver"] == FileSolver.UMAP.value: 
            embeddings = UMAP().transform(data["files"], data["data"]["module"], data["data"]["task"])
        else:
            embeddings = UMAP().transform(data["files"], data["data"]["module"], data["data"]["task"])

        hdbscan = HDBSCAN()
        hdbscan.fit(embeddings)
        hover_data = create_processed_df(embeddings, hdbscan.cluster, data)
        return hover_data
        