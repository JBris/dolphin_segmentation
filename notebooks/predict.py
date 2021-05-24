######################################################################################
## Code is based on a facenet implementation: https://github.com/sainimohit23/FaceNet-Real-Time-face-recognition
## Code was amended for the use of this project

import os
import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("tensorflow").addHandler(logging.NullHandler(logging.ERROR))
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'

from keras import backend as K
#from tensorflow.keras.layers import Layer, InputSpec
import tensorflow.python.keras.engine
import tensorflow as tf

K.set_image_data_format('channels_first')
import cv2
import numpy as np
#from numpy import genfromtxt
import pandas as pd

from fr_utils import *
from inception_blocks_v2 import *
import imutils
from parameters import *
#import pickle
import sys
from pathlib import Path
from detect import *
import pickle

# =============================================================================
# np.set_printoptions(threshold=np.nan)
# =============================================================================
import keras


image_dirs = Path(TARGET_IMAGES_DIR) 
images_trn = pd.DataFrame(columns=['label', 'path', 'name', 'img'], dtype=object)
print("dir:" + TARGET_IMAGES_DIR)

with tf.Graph().as_default():
        gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.5)
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.compat.v1.Session(config=config)
        
best_model_path =""
if(os.path.exists("bestmodel.txt")):
    with open('bestmodel.txt', 'r') as file:
        best_model_path = file.read()
    
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
    
    
if(len(fins) == 0):
    print("No images found in database!!")
    print("Please add images to database")
    sys.exit()

if os.path.exists(best_model_path) and best_model_path !="":
    print("Trained model found")
    print("Loading custom trained model...")
    FRmodel = keras.models.load_model(best_model_path,custom_objects={'triplet_loss': triplet_loss}, compile=False)

else:
    print("Custom trained model not found, exiting...")
    exit(0)

def verify(image_path, identity, database, model):    
    encoding = img_to_encoding(image_path, model, False)
    mdist = 1000
    for pic in database:
        dist = np.linalg.norm(encoding - pic)
        if dist < mdist:
            mdist = dist
    #print(identity + ' : ' +str(mdist)+ '<>'+str(dist)+ ' ' + str(len(database)))
    
    detect= True if mdist<THRESHOLD else False

    return mdist, detect

database = {}

if os.path.exists(DICTPATH) and DICTPATH !="":
    print("Loading fin data...")
    database = pickle.load(open(DICTPATH, 'rb'))
else:
    for fin in fins:
        database[fin] = []
        for i, file in enumerate(images_trn[images_trn.label==fin].itertuples()):
            database[fin].append(img_to_encoding(str(file.path), FRmodel))
    pickle.dump(database, open(DICTPATH, 'wb'))

        
manual_adj=False
testmode=False

# if manual_adj:
#     cv2.namedWindow("adjustments", cv2.WINDOW_AUTOSIZE)
#     cv2.namedWindow("source", cv2.WINDOW_AUTOSIZE)
img_process = {}
if testmode:
    fname="NDD20/data/5.jpg"
    image = cv2.imread(IMG_DIR+fname)
    if manual_adj:
        img, cnt = get_fin(image,0,manual_adj)  
        cv2.destroyAllWindows()
        #cv2.waitKey()  
        img_process.update({fname : det})
    else:
        img, cnt = get_fin(image,0,manual_adj)  
        #img = cv2.imread(IMG_DIR+"fin_features_512/0002/pre1_HG_090329_0030_NB_rsz_0002.png")
        #img = cv2.imread(IMG_DIR+"fin_features_512/0014/pre1_HG_111220_161_E1_JQ_N1_rsz_0014.png")
        # img = cv2.imread(IMG_DIR+"fin_features_512/0075/pre1_HG_120210_061_SD_rsz_0075.png")
        #img = cv2.imread(INPUT_DIR+"/pre1_HG_111006_031_E1_N2_rsz_0204.png")
        #fname="test 0002"
        #img = cv2.imread(IMG_DIR+"final_to_match/HG_140530_049_KM_N12.JPG")
        #img = cv2.imread(IMG_DIR+"final_pigmentation_catalogue_2016/0055/HG_130208_303_E1_KR_AII.PNG")
        #img = cv2.imread(IMG_DIR+"fin_features_512/0014/pre1_HG_111220_161_E1_JQ_N1_ftr_0014.png")
    det = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    det = cv2.resize(det,(IMAGE_SIZE, IMAGE_SIZE))
    img_process.update({fname : det})
else:
    for fname in os.listdir(INPUT_DIR):
        fpath = os.path.join(INPUT_DIR, fname)
        
        #below line if testing pre-cropped images without detection
        #img = cv2.imread(fpath)
        
        #below lines if using raw images needing detection
        image = cv2.imread(fpath)
        img, cnt = get_fin(image,0,False)  

        if cnt==0:
            print("Noting found: " + fpath)
            continue
        
        det = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        det = cv2.resize(det,(IMAGE_SIZE, IMAGE_SIZE))
        img_process.update({fname : det})

# let's detect it

for fname,det in img_process.items():
    identity = ""
    detected  = False
    min_dist = 1000
    for fin in range(len(fins)):
        dolphin = fins[fin]
        # det = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # det = cv2.resize(det,(IMAGE_SIZE, IMAGE_SIZE))
        dist, detected = verify(det, dolphin, database[dolphin], FRmodel )
        #print("Detected: " +str(dist) + " < " + str(min_dist))
        if detected and dist<min_dist:
            min_dist = dist
            identity = dolphin
    if detected:
        #cv2.rectangle(img, (20, 20), (img.shape[0]-20, img.shape[1]-20), (0, 255, 50), 2)
        #cv2.putText(img, identity, (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        print("Matched: " +fname + " = " + str(identity))

# cv2.imshow('fin', img)
# cv2.waitKey()
# cv2.destroyAllWindows()
