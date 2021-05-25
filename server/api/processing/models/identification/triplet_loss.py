import triplet_loss_helper
from umap import UMAP

class TripletLoss:

    def transform(self, files, module, task):
        model = triplet_loss_helper.load_model()
        files = triplet_loss_helper.process_files(files)
        embeddings = model.predict(files)
        return UMAP(100).fit_transform(embeddings)
        