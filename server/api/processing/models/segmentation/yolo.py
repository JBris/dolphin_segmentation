import cv2
import numpy as np

from pathlib import Path
from scipy.spatial import distance

class YOLO:
    IMG_SIZE = 256
    CONFIDENCE_THRESHOLD = 0.3

    def segment(self, data, write_to_file = True):
        model_path = f"/app/models/{data['data']['module']}"
        darknet = cv2.dnn.readNetFromDarknet(f"{model_path}/yolov4.cfg", f"{model_path}/yolov4_best.weights")

        for file in data["files"]:
            segmented_image = self.crop_image(file, darknet)
            if write_to_file: cv2.imwrite(f"{data['data']['out']}/{Path(file).stem}.png", segmented_image)
        return data

    def crop_image(self, file, net):
        image = cv2.imread(file)
        (H, W) = image.shape[:2]

        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (self.IMG_SIZE, self.IMG_SIZE), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        
        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:

            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > self.CONFIDENCE_THRESHOLD:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.CONFIDENCE_THRESHOLD, self.CONFIDENCE_THRESHOLD)
        dims = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                dims.append((y, y + h, x, x + w))
        dim = dims[0]
        image = image[dim[0]:dim[1], dim[2]:dim[3]]
        return image

