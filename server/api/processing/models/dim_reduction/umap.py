from joblib import load as model_load

from api.services.file_select import FileTask

def identify(images, module):
    model = model_load(f"/app/models/{module}/umap.joblib")
    embeddings = model.transform(images)
    return embeddings

def classify(images, module):
    model = model_load(f"/app/models/{module}/umap.joblib")
    embeddings = model.transform(images)
    return embeddings

class UMAP:
    def transform(self, images, module, task):
        if task == FileTask.IDENTIFICATION.value:
            return identify(images, module)
        else:
            return classify(images, module)
