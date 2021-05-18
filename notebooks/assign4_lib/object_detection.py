import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from glob import glob
import shutil
import tensorflow as tf

def draw_bounding_box(net, IMG_SIZE, CONFIDENCE_THRESHOLD, test_image, preprocess = False):
    image = cv2.imread(test_image)
    
    if preprocess:
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        image = cv2.bilateralFilter(image, 9, 50, 50)
        
    (H, W) = image.shape[:2]
    LABELS = ["dolphin"]
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (IMG_SIZE, IMG_SIZE))
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:

        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, CONFIDENCE_THRESHOLD)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)

    plt.imshow(image, cmap='gray')


def preprocess_image(file, IMG_SIZE):
    fig, axs = plt.subplots(1, 2, constrained_layout = False)
    #image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    image = cv2.imread(file)
    axs[0].imshow(image)
    axs[0].set_title("Pre-processed")
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image = cv2.bilateralFilter(image, 9, 50, 50)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
     
    #image = cv2.fastNlMeansDenoising(image, None, 10)
    #image = cv2.GaussianBlur(image, (5, 5), 0)
    
#     _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
#     img_contours = sorted(img_contours, key=cv2.contourArea)

#     for i in img_contours:
#         if cv2.contourArea(i) > 100: break
    
#     mask = np.zeros(image.shape[:2], np.uint8)
#     cv2.drawContours(mask, [i],-1, 255, -1)
#     image = cv2.bitwise_and(image, image, mask=mask)
    axs[1].imshow(image, cmap='gray')
    axs[1].set_title("Processed")

def crop_image(net, IMG_SIZE, CONFIDENCE_THRESHOLD, test_image, preprocess = False):
    image = cv2.imread(test_image)
    
    if preprocess:
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        image = cv2.bilateralFilter(image, 9, 50, 50)
        
    (H, W) = image.shape[:2]

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (IMG_SIZE, IMG_SIZE))
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:

        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, CONFIDENCE_THRESHOLD)
    dims = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            dims.append((y, y + h, x, x + w))
    dim = dims[0]
    image = image[dim[0]:dim[1], dim[2]:dim[3]]
    plt.imshow(image, cmap='gray')
    return dim