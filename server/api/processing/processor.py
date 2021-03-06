import numpy as np
import pandas as pd

from api.processing.models.clustering.hdbscan import HDBSCAN
from api.processing.models.dim_reduction.umap import UMAP
from api.processing.models.identification.triplet_loss import TripletLoss
from api.processing.models.segmentation.yolo import YOLO

from api.services.file_select import FileTask, FileSolver

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
 
    def segment(self, data):
        if data["data"]["solver"] == FileSolver.YOLO.value: return YOLO().segment(data)
        else: return YOLO().segment(data)

    def process(self, data, current_task):
        current_task.update_state(state = "PROGRESS", meta = {"step": "Processing images", "step_num": 2, "step_total": 4, "substeps": 0})
        if data["data"]["task"] == FileTask.SEGMENTATION.value: return self.segment(data)

        if data["data"]["solver"] == FileSolver.UMAP.value: embeddings = UMAP().transform(data["files"], data["data"]["module"], data["data"]["task"])
        elif data["data"]["solver"] == FileSolver.TRIPLET_LOSS.value: embeddings = TripletLoss().transform(data["files"], data["data"]["module"], data["data"]["task"])
        else: embeddings = UMAP().transform(data["files"], data["data"]["module"], data["data"]["task"])

        hdbscan = HDBSCAN()
        hdbscan.fit(embeddings)
        hover_data = create_processed_df(embeddings, hdbscan.cluster, data)
        return hover_data
        