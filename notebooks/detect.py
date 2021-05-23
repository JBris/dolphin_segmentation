# -*- coding: utf-8 -*-
"""
Created on Wed May 19 07:19:19 2021

@author: elMartino
"""

import cv2
import json 
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import random
import re
import seaborn as sns
import skimage 
from skimage import exposure

import math
from scipy.interpolate import splprep, splev

import time

from skimage.exposure import rescale_intensity
from skimage.io import imread, imsave
from pathlib import Path

# helper methods for feature extraction
from feature_extract import *

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
import sys
from parameters import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt static label demo")
        width = 640
        height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        # create a text label
        self.textLabel = QLabel('Demo')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        # create a grey pixmap
        grey = QPixmap(width, height)
        grey.fill(QColor('darkGray'))
        # set the image image to the grey pixmap
        self.image_label.setPixmap(grey)


#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    a = App()
#    a.show()
#    sys.exit(app.exec_())

IMG_SIZE = 512
# IMG_DIR = '../images/'
# IMAGES_DIR = IMG_DIR+'final_pigmentation_catalogue_2016'
# TARGET_IMAGES_DIR = IMG_DIR+'fin_features'
# MAX_FILES = 50

# MODEL_DIR="../models/darknet"



#####################################################################################
#####################################################################################

def filter(img,thrsh_a,thrsh_b,canny_a,canny_b,canny_c, rem_bkg=False):
    fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
    
    img_in = img.copy()

    
    fgmask = fgbg.apply(img_in)
    #cv2.imshow("source", fgmask)
    
    img_tmp = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)      

    
    # Contrast stretching
    p1, p2 = np.percentile(img_tmp, (2, 98))
    img_tmp = exposure.rescale_intensity(img_tmp, in_range=(p1, p2))
    
    #blur to reduce noise
#     cv2.blur(img_tmp, (18, 18))    
    cv2.GaussianBlur(img_tmp, (15, 15), 0)
    img_tmp = claheGray(img_tmp, 1.8,8)
    
    ret,thresh = cv2.threshold(img_tmp,math.floor(np.average(img_tmp)),thrsh_b,cv2.THRESH_BINARY_INV)
    img_tmp=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
    #kernel = np.ones((9, 9), np.uint8)
    img_tmp = cv2.dilate(img_tmp, None, iterations=2)
    img_tmp = cv2.erode(img_tmp, None, iterations=2)
    

    # create binary mask and clean away some spots
    _,img_tmp = cv2.threshold(img_tmp, thrsh_a, thrsh_b, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    img_tmp = cv2.erode(img_tmp, kernel, iterations=3)
    img_tmp = cv2.dilate(img_tmp, kernel, iterations=3)  
    #img_bin = (255-img_bin)
#    cv2.imshow("source", fgmask)
        
    # contour - get the contour from the mask
    img_c, cntr, contours,edges = drawContour(img,img_tmp,False,100,1,1,canny_a,canny_b,canny_c,7)
    #contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    # remove background
    if rem_bkg:
        cv2.drawContours(img_in, contours, -1, (0,255,0), -1) 
#    img_in = cv2.erode(img_in, None, iterations=1)
#    img_in = cv2.dilate(img_in, None, iterations=1)
    # create mask
    img_mask = np.zeros((img_in.shape[0], img_in.shape[1]), np.uint8)
    cv2.drawContours(img_mask, contours, -1, (255,255,255), -1) 
    #kernel = np.ones((3, 3), np.uint8)
    img_mask = cv2.erode(img_mask, None, iterations=1)
    img_mask = cv2.dilate(img_mask, None, iterations=1)
    
    #img_cntr = np.zeros((img_in.shape[0], img_in.shape[1]), np.uint8)
    #cv2.drawContours(img_cntr, contours, 1, (255,255,255), -1) 
    img_mask = (255-img_mask)
    #cv2.imshow("source", img_mask)
    
    return img_in, img_mask, cntr

#####################################################################################

def filter_mask(img,thrsh_a,thrsh_b,canny_a,canny_b,canny_c):
    fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
    
    img_in = img.copy()
    xp = [65, 60, 200, 200, 250]
    fp = [0, 45, 200, 200, 0]

    x = np.arange(256)
    table = np.interp(x, xp, fp).astype('uint8')
    #img_tmp = cv2.LUT(img_in, table)
    
    fgmask = fgbg.apply(img_in)
    #cv2.imshow("source", fgmask)
    #hsv = cv2.cvtColor(img_in, cv2.COLOR_BGR2HSV) 
    #maskc = cv2.inRange(hsv, color_tracked_lower, color_tracked_upper) 
    #maskc = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
    
    img_tmp = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)      

    
    # Contrast stretching
    p1, p2 = np.percentile(img_tmp, (2, 98))
    img_tmp = exposure.rescale_intensity(img_tmp, in_range=(p1, p2))
    
    #blur to reduce noise
#     cv2.blur(img_tmp, (18, 18))    
    cv2.GaussianBlur(img_tmp, (15, 15), 0)
    img_tmp = claheGray(img_tmp, 1.8,8)
    
    ret,thresh = cv2.threshold(img_tmp,math.floor(np.average(img_tmp)),thrsh_b,cv2.THRESH_BINARY_INV)
    img_tmp=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
    #kernel = np.ones((9, 9), np.uint8)
    img_tmp = cv2.dilate(img_tmp, None, iterations=2)
    img_tmp = cv2.erode(img_tmp, None, iterations=2)
    

    # create binary mask and clean away some spots
    _,img_tmp = cv2.threshold(img_tmp, thrsh_a, thrsh_b, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    img_tmp = cv2.erode(img_tmp, kernel, iterations=3)
    img_tmp = cv2.dilate(img_tmp, kernel, iterations=3)  
    #img_bin = (255-img_bin)
#    cv2.imshow("source", fgmask)
        
    # contour - get the contour from the mask
    img_c, cntr, contours,edges = drawContour(img,img_tmp,False,100,1,1,canny_a,canny_b,canny_c,7)
    #contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    # remove background
    cv2.drawContours(img_in, contours, -1, (0,255,0), -1) 
#    img_in = cv2.erode(img_in, None, iterations=1)
#    img_in = cv2.dilate(img_in, None, iterations=1)
    # create mask
    img_mask = np.zeros((img_in.shape[0], img_in.shape[1]), np.uint8)
    cv2.drawContours(img_mask, contours, -1, (255,255,255), -1) 
    #kernel = np.ones((3, 3), np.uint8)
    img_mask = cv2.erode(img_mask, None, iterations=1)
    img_mask = cv2.dilate(img_mask, None, iterations=1)
    
    #img_cntr = np.zeros((img_in.shape[0], img_in.shape[1]), np.uint8)
    #cv2.drawContours(img_cntr, contours, 1, (255,255,255), -1) 
    img_mask = (255-img_mask)
    #cv2.imshow("source", img_mask)
    
    return img_in, img_mask, cntr


#####################################################################################
#####################################################################################


def get_fin(image,idx=0,MASK=False):
    # cv2.namedWindow("source1", cv2.WINDOW_AUTOSIZE)
    # imS = cv2.resize(image, (960, 540))  
    # cv2.imshow("source1", imS)
    # cv2.waitKey(0)
    #cv2.destroyWindow("source1")
    # image = resizeAndPad(image, (720,1000), 255)
    
    # cv2.namedWindow("source", cv2.WINDOW_AUTOSIZE)
    
    CONFIDENCE = 0.5
    THRESHOLD = 0.5
    
    weightsPath = os.path.sep.join([MODEL_DIR, "training/yolov4-dolphin_best.weights"])
    configPath = os.path.sep.join([MODEL_DIR, "yolov4-dolphin.cfg"])
    
    img_fins, _ = find_fin(image,weightsPath,configPath,CONFIDENCE,THRESHOLD,IMG_SIZE,0)
    
    #print(len(img_fins))
    if len(img_fins)>0:
        img = img_fins[idx][0] # list of lists sorted by size - first entry = image, second = eucl-dist as size
    else:
        return None, 0
    # add border
    img = add_border(img,5,0)
    
    # create mask for border and pad area
    mask_blk = cv2.inRange(img, np.asarray([0, 0, 0]),np.asarray([0, 0, 0 ]))
    
    if not MASK:
        res = cv2.convertScaleAbs(img, alpha=0.95, beta=-40)
        #print(beta)
        lookUpTable = np.empty((1,256), np.uint8)
        for i in range(256):
            lookUpTable[0,i] = np.clip(pow(i / 255.0, 0.4) * 255.0, 0, 255)
        img_impr = cv2.LUT(res, lookUpTable)            
        img_correctedb, img_mask, img_cntr = filter(img_impr,180,255,75,100,15,False)  
        # add mask for border    img_mask = img_mask+mask_blk
        
        # merge channels adding the white mask to get rid of backgounds hidden behind alpha mask
        b, g, r = cv2.split(img_impr)
        a = np.zeros((IMG_SIZE, IMG_SIZE), np.uint8)
        image = cv2.merge([cv2.subtract(b,mask_blk), cv2.subtract(g,mask_blk), cv2.subtract(r,mask_blk)])
        
        # features
        image_x = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        img_rsz, image_ftr, img_mask, img_cntr, img_fd, fourier_desc, status = feature_extract(image_x, IMG_SIZE)
        #image_ftr = cv2.cvtColor(image_ftr, cv2.COLOR_BGRA2BGR)
        # cv2.imshow("source", image_ftr)
        return image_ftr, len(img_fins)
    else: 
        image = img
        cv2.namedWindow("adjustments", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("source", cv2.WINDOW_AUTOSIZE)
        
        alpha = 0.95
        alpha_max = 500
        beta = -60
        beta_max = 150
        gamma = 0.60
        gamma_max = 200
        
        img_alpha = 0.95
        img_beta = -60
        img_gamma = 0.60
        
        
        bin_thrsa = 55
        bin_thrsb = 255
        
        canny_a = 0.75
        canny_b = 0.5
        canny_c = 0.05
        
        is_invers = 0
                      
        def basicLinearTransform():
            resa = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            res = cv2.convertScaleAbs(img, alpha=img_alpha, beta=img_beta)
            print(beta)
            lookUpTablea = np.empty((1,256), np.uint8)
            lookUpTable = np.empty((1,256), np.uint8)
            for i in range(256):
                lookUpTablea[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
                lookUpTable[0,i] = np.clip(pow(i / 255.0, img_gamma) * 255.0, 0, 255)
            img_maska = cv2.LUT(resa, lookUpTablea)
            img_impr = cv2.LUT(res, lookUpTable)
    
            img_correctedb, img_mask, img_cntr = filter_mask(img_maska,bin_thrsa,bin_thrsb,canny_a,canny_b,canny_c)
            if is_invers==1:
                img_mask = (255-img_mask)         
        
            # add mask for border
            img_mask = img_mask+mask_blk
            
            # merge channels adding the white mask to get rid of backgounds hidden behind alpha mask
            b, g, r = cv2.split(img_impr)
            #a = np.zeros((IMG_SIZE, IMG_SIZE), np.uint8)
            image = cv2.merge([cv2.subtract(b,img_mask), cv2.subtract(g,img_mask), cv2.subtract(r,img_mask)])
    
            
            # features
            image_x = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2BGRA)
            img_rsz, image_ftr, img_mask, img_cntr, img_fd, fourier_desc, status = feature_extract(image_x, IMG_SIZE)
            #image_ftr = cv2.cvtColor(image_ftr, cv2.COLOR_BGRA2BGR)
            cv2.imshow("source", image_ftr)
            img_corrected = cv2.hconcat([image, img_correctedb])
            cv2.imshow("adjustments", img_corrected)
            
        
        def on_linear_transform_alpha_trackbar(val):
            global alpha
            alpha = val / 100
            basicLinearTransform()
        
        def on_linear_transform_beta_trackbar(val):
            global beta
            beta = val - 100
            basicLinearTransform()
        
        def on_gamma_correction_trackbar(val):
            global gamma
            gamma = val / 100
            basicLinearTransform()
            
        def img_alpha_trackbar(val):
            global img_alpha
            img_alpha = val / 100
            basicLinearTransform()
        
        def img_beta_trackbar(val):
            global img_beta
            img_beta = val - 100
            basicLinearTransform()
        
        def img_gamma_trackbar(val):
            global img_gamma
            img_gamma = val / 100
            basicLinearTransform()
            
        def on_bina_adjust_trackbar(val):
            global bin_thrsa
            bin_thrsa = val
            basicLinearTransform()
        
        def on_binb_adjust_trackbar(val):
            global bin_thrsb
            bin_thrsb = val
            basicLinearTransform()
            
        def on_canny_a_adjust_trackbar(val):
            global canny_a
            canny_a = val
            basicLinearTransform()
            
        def on_canny_b_adjust_trackbar(val):
            global canny_b
            canny_b = val
            basicLinearTransform()  
        
        def on_canny_c_adjust_trackbar(val):
            global canny_c
            canny_c = val
            basicLinearTransform()
            
        def setMask(val):
            global is_invers 
            is_invers=val
            basicLinearTransform()
        
        img_corrected = np.empty((img.shape[0], img.shape[1]*2, img.shape[2]), img.dtype)
        img_gamma_corrected = np.empty((img.shape[0], img.shape[1]*2, img.shape[2]), img.dtype)
        
        # cv2.namedWindow("adjustments", cv2.WINDOW_AUTOSIZE)
        # cv2.namedWindow("source", cv2.WINDOW_AUTOSIZE)
        # cv2.namedWindow('Gamma correction')
        
        alpha_init = int(alpha *100)
        cv2.createTrackbar('Alpha gain (contrast)', 'adjustments', alpha_init, alpha_max, on_linear_transform_alpha_trackbar)
        beta_init = beta + 100
        cv2.createTrackbar('Beta bias (brightness)', 'adjustments', beta_init, beta_max, on_linear_transform_beta_trackbar)
        gamma_init = int(gamma * 100)
        cv2.createTrackbar('Gamma correction', 'adjustments', gamma_init, gamma_max, on_gamma_correction_trackbar)
        
        img_alpha_init = int(img_alpha *100)
        cv2.createTrackbar('Alpha Img', 'adjustments', img_alpha_init, alpha_max, img_alpha_trackbar)
        img_beta_init = img_beta + 100
        cv2.createTrackbar('Beta Img', 'adjustments', img_beta_init, beta_max, img_beta_trackbar)
        img_gamma_init = int(img_gamma * 100)
        cv2.createTrackbar('Gamma Img', 'adjustments', img_gamma_init, gamma_max, img_gamma_trackbar)
        
        
        bina_init = int(bin_thrsa)
        cv2.createTrackbar('Binary Threshold a', 'adjustments', bina_init, 255, on_bina_adjust_trackbar)
        binb_init = int(bin_thrsb)
        cv2.createTrackbar('Binary Threshold b', 'adjustments', binb_init, 255, on_binb_adjust_trackbar)
        
        # canny_a_init = int(canny_a*100)
        # cv2.createTrackbar('Canny Threshold a', 'adjustments', canny_a_init, 255, on_canny_a_adjust_trackbar)
        # canny_b_init = int(canny_b*100)
        # cv2.createTrackbar('Canny Threshold b', 'adjustments', canny_b_init, 255, on_canny_b_adjust_trackbar)
        # canny_c_init = int(canny_c*100)
        # cv2.createTrackbar('Canny Threshold c', 'adjustments', canny_c_init, 7, on_canny_c_adjust_trackbar)
        
        #cv2.createButton("Set Maks",setMask,NULL,cv2.QT_PUSH_BUTTON,1)
        
        
        on_linear_transform_alpha_trackbar(alpha_init)
        on_gamma_correction_trackbar(gamma_init)
        on_bina_adjust_trackbar(bina_init)
        on_binb_adjust_trackbar(binb_init)
        # on_canny_a_adjust_trackbar(canny_a_init)
        # on_canny_b_adjust_trackbar(canny_b_init)
        # on_canny_c_adjust_trackbar(canny_c_init)
        
        img_alpha_trackbar(img_alpha_init)
        #img_beta_trackbar(img_beta_init)
        img_gamma_trackbar(img_gamma_init)
        
        # create switch for ON/OFF functionality
        switch = '0 : OFF \n1 : ON'
        cv2.createTrackbar(switch, 'adjustments',0,1,setMask)
            
        while True:  
            c = cv2.waitKey(0)
            if 'q' == chr(c & 255):
                return image, len(img_fins)
            

# image = cv2.imread(IMG_DIR+"NDD20/data/9.jpg")
# img = get_fin(image,2,False)    
# cv2.waitKey()
# cv2.destroyAllWindows() 
    
