######################################################################################
## Code is based on a facenet implementation: https://github.com/sainimohit23/FaceNet-Real-Time-face-recognition
## Code was amended for the use of this project

mport os
import cv2
import numpy as np
import pandas as pd
from parameters import *
import pickle
from pathlib import Path


image_dirs = Path(TARGET_IMAGES_DIR) 
images_trn = pd.DataFrame(columns=['label', 'path', 'name', 'img'], dtype=object)

labels =[]
for image_dir in image_dirs.glob('*'):
    label = image_dir.stem
    labels.append(label)
    for file in image_dir.glob('*'+trn_img+'*'):
        basename = os.path.basename(file)
        f_name, f_ext = os.path.splitext(basename)
        if f_ext.lower() != ".png" or f_name[0:4] !="pre1": continue
        images_trn.loc[len(images_trn)] = [label, file, f_name, ""]
    if len(images_trn) >= MAX_FILES: break

paths={}
fins=[]
for i, label in enumerate(labels): 
    paths[label] = TARGET_IMAGES_DIR.replace("\\", "/")+"/"+label
    fins.append(label)
    
input_shape = (3, IMAGE_SIZE, IMAGE_SIZE)
    
images = {}


for key in paths.keys():
    li = []
    for i, file in enumerate(images_trn[images_trn.label==key].itertuples()):
        img1 = cv2.imread(str(file.path))
        img2 = img1[...,::-1]
        li.append(np.around(np.transpose(img2, (2,0,1))/255.0, decimals=12))
    images[key] = np.array(li)
    
def batch_generator(batch_size=16):
    y_val = np.zeros((batch_size, 2, 1))
    anchors = np.zeros((batch_size, input_shape[0], input_shape[1], input_shape[2]))
    positives = np.zeros((batch_size, input_shape[0], input_shape[1], input_shape[2]))
    negatives = np.zeros((batch_size, input_shape[0], input_shape[1], input_shape[2]))
    
    while True:
        for i in range(batch_size):
            positivefin = fins[np.random.randint(len(fins))]
            negativefin = fins[np.random.randint(len(fins))]
            while positivefin == negativefin:
                negativefin = fins[np.random.randint(len(fins))]

            positives[i] = images[positivefin][np.random.randint(len(images[positivefin]))]
            anchors[i] = images[positivefin][np.random.randint(len(images[positivefin]))]
            negatives[i] = images[negativefin][np.random.randint(len(images[negativefin]))]
        
        x_data = {'anchor': anchors,
                  'anchorPositive': positives,
                  'anchorNegative': negatives
                  }
        
        yield (x_data, [y_val, y_val, y_val])