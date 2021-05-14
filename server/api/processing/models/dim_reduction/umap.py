import cv2
import numpy as np

from joblib import load as model_load

from api.services.file_select import FileTask

def preprocess_images(image_files, img_size):
    images = []

    for file in image_files:
        img = cv2.imread(file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (img_size, img_size))
        img = img.astype('float32')
        img = cv2.bilateralFilter(img, 9, 50, 50)
    #     #image = cv2.normalize(image, np.zeros((img_size, img_size)), 0, 1, cv2.NORM_MINMAX)
        images.append(img)
    images = np.asarray(images)
    images = images.reshape((images.shape[0], -1))
    return images

def identify(images, module):
    model = model_load(f"/app/models/{module}/umap_identify.joblib")
    embeddings = model.transform(images)
    return embeddings

def classify(images, module):
    model = model_load(f"/app/models/{module}/umap_classify.joblib")
    embeddings = model.transform(images)
    return embeddings

class UMAP:
    IMG_SIZE = 256

    def transform(self, files, module, task):
        images = preprocess_images(files, self.IMG_SIZE)
        if task == FileTask.IDENTIFICATION.value: return identify(images, module)
        if task == FileTask.CLASSIFICATION.value : return classify(images, module)
        else: raise NotImplementedError(f"UMAP has not implemented task: {task}")
