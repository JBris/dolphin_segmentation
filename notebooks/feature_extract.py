# -*- coding: utf-8 -*-
"""
Assignment 4
Helper methods for image feature extraction
@author: Martin BRenner

"""
import cv2
import numpy as np
from skimage.filters import threshold_yen
from skimage.exposure import rescale_intensity
from scipy.interpolate import splprep, splev
from scipy.spatial import distance
from skimage.io import imread, imsave
from pathlib import Path

#https://stackoverflow.com/questions/44720580/resize-image-canvas-to-maintain-square-aspect-ratio-in-python-opencv
def resizeAndPad(img, size, padColor=0):
    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
#         pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_top, pad_bot = np.floor(pad_vert).astype(int) + np.ceil(pad_vert).astype(int),0
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
        padColor = [padColor]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)
    return scaled_img

def add_border(img,bordersize=10,color=[255,255,255]):
    border = cv2.copyMakeBorder(
        img,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=color
    )
    return border

def contrast_yt(img,a=0,b=0,c=255,ytfactor=0.5):
    yt = threshold_yen(img)
    img = rescale_intensity(img, (a, yt*ytfactor), (b, c))
    return img

def claheHSV(img,c,g):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv_image)
    clahe = cv2.createCLAHE(clipLimit=c, tileGridSize=(g,g))
    v = clahe.apply(v)
    hsv_image = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

def claheGray(img,c,g):
    clahe = cv2.createCLAHE(clipLimit=c, tileGridSize=(g,g))
    return clahe.apply(img)

def drawContour(img,mask,smooth=False,sv=100,d=8,de=6, ka=50, kb=50, kc=5, kk=1):
    cntr = np.zeros(mask.shape, np.uint8)
    # Use Canny to detect edges
    edges = cv2.Canny(mask, ka, kb, kc)
    # Dilate and erode to thicken the edges
    kernel = np.ones((kk, kk), np.uint8)
    
    edges = cv2.dilate(edges, kernel, iterations = de)
    edges = cv2.erode(edges, kernel, iterations = de)
    
    # RETR_EXTERNAL RETR_TREE
    
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # CHAIN_APPROX_SIMPLE CHAIN_APPROX_NONE  
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    img_l = img.copy()
    #print("ka: "+ str(ka))
    smoothened = []
    if smooth:
        for contour in contours:
            x,y = contour.T
            # Convert from numpy arrays to normal arrays
            x = x.tolist()[0]
            y = y.tolist()[0]
            tck, u = splprep([x,y], u=None, s=1.0, per=1)
            u_new = np.linspace(u.min(), u.max(), sv) # <<<smoothness
            x_new, y_new = splev(u_new, tck, der=0)
            # Convert it back to numpy format for opencv to be able to display it
            res_array = [[[int(i[0]), int(i[1])]] for i in zip(x_new,y_new)]
            smoothened.append(np.asarray(res_array, dtype=np.int32))
        cv2.drawContours(img_l, smoothened, -1, (0,0,0), d)
    else:
        cv2.drawContours(img_l, contours, -1, (0,0,0), d)
    cv2.drawContours(cntr, contours, -1, (255,255,255), d)    
    return img_l, cntr, contours, edges


##################################################################
## Fourier-Descriptor 

def findDescriptor(contour):
    # finds and returns the Fourier-Descriptor of the contour
    if len(contour)>0:
        contour_array = contour[0][:, 0, :]
        contour_complex = np.empty(contour_array.shape[:-1], dtype=complex)
        contour_complex.real = contour_array[:, 0]
        contour_complex.imag = contour_array[:, 1]
        fourier_result = np.fft.fft(contour_complex)
        return fourier_result
    else:
        return []

def truncate_descriptor(descriptors, degree):
    # truncate an unshifted fourier descriptor array
    descriptors = np.fft.fftshift(descriptors)
    center_index = round(len(descriptors) / 2)
    #print("ci:" + str(center_index) + " : " + str(center_index - degree / 2) + " : " + str(center_index + degree / 2))
    descriptors = descriptors[int(center_index - degree / 2):int(center_index + degree / 2)]
    descriptors = np.fft.ifftshift(descriptors)
    return descriptors

def reconstruct(descriptors, degree, IMG_SIZE):
    # truncate the long list of descriptors to certain length
    # not stable - disabled
    # descriptor_in_use = truncate_descriptor(descriptors, degree)
    descriptor_in_use = descriptors
    contour_reconstruct = np.fft.ifft(descriptor_in_use)
    contour_reconstruct = np.array(
        [contour_reconstruct.real, contour_reconstruct.imag])
    contour_reconstruct = np.transpose(contour_reconstruct)
    contour_reconstruct = np.expand_dims(contour_reconstruct, axis=1)
    # make positive
    if contour_reconstruct.min() < 0:
        contour_reconstruct -= contour_reconstruct.min()
    # normalization
    contour_reconstruct *= IMG_SIZE / contour_reconstruct.max()
    # type cast to int32
    contour_reconstruct = contour_reconstruct.astype(np.int32, copy=False)
    img_fdsc = np.zeros((IMG_SIZE, IMG_SIZE), np.uint8)
    # draw and visualize
    cv2.drawContours(img_fdsc, contour_reconstruct, -1, 255, thickness=4)
    return img_fdsc, descriptor_in_use

#########################################################################
### YOLO
def find_fin(image,weightsPath,configPath, CONFIDENCE = 0.5, THRESHOLD = 0.3,img_size=512,pad_col=0):   
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    img_find = image.copy()
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)
    # show timing information on YOLO
    
    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []
    
    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > CONFIDENCE:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                
    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE,THRESHOLD)
                # ensure at least one detection exists
    images=[]
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        images = []
        colors = np.random.randint(0, 255, size=(len(idxs), 3), dtype='uint8')
        #img_sizes = [] 
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in colors[classIDs[i]]]
            crop_img = image[y:y+h, x:x+w]
            #img_sizes.append(distance.euclidean((y,y+h),(x,x+w)))
            cv2.rectangle(img_find, (x, y), (x + w, y + h), [0,255,255], 6)
            text = "{}: {:.4f}".format("Dolphin", confidences[i])
            cv2.putText(img_find, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,1.5, color, 4)
            crop_img = resizeAndPad(crop_img, (img_size,img_size), pad_col)
            images.append([crop_img,distance.euclidean((y,y+h),(x,x+w))])
    #         cv2.imshow("cropped", crop_img)
    images.sort(reverse=True, key = lambda i: i[1]) # largest image first
    return images, img_find

def feature_extract(img_in, IMG_SIZE):
    try:
        img_rsz = resizeAndPad(img_in, (IMG_SIZE,IMG_SIZE), 255)
    except:
        return None, None, None, None, None, None, 3    
    # add border
    # img_rsz = add_border(img_rsz,5,0)
    # split and extract alpha
    try:
        b, g, r, a = cv2.split(img_rsz)
    except:
        return None, None, None, None, None, None, 1
    img_a = (255-a) # make a white mask
    
    _,a2 = cv2.threshold(img_a, 170, 255, cv2.THRESH_BINARY)
    # merge channels adding the white mask to get rid of backgounds hidden behind alpha mask
    img_in = cv2.merge([cv2.add(b,a2), cv2.add(g,a2), cv2.add(r,a2)],a)
    
    img_rsz = img_in.copy() # send back fixed resized image
    # create binary mask and clean away some spots
    _,a3 = cv2.threshold(img_a, 20, 255, cv2.THRESH_BINARY_INV)
#     kernel = np.ones((2, 2), np.uint8)
    a3 = cv2.erode(a3, None, iterations=2)
    a3 = cv2.dilate(a3, None, iterations=2)
    
    try:
        #img_in = claheHSV(img_in)
        # make gray
        img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    
        #contrast stretching
        xp = [40, 80, 200, 200, 200]
        fp = [0, 80, 200, 200, 200]
        x = np.arange(256)
        table = np.interp(x, xp, fp).astype('uint8')
        #img_in = cv2.LUT(img_in, table)
    
        cv2.bilateralFilter(img_in, 3, 50, 50)
    
        #blur to reduce noise
        cv2.blur(img_in, (18, 18))    
        #cv2.GaussianBlur(img_in, (11, 11), 0)
        
        # apply CLAHE
        img_in = claheGray(img_in, 1.5,8)
        
        # contrast
    #    img_in = contrast_yt(img_in,30,0,255)
    
        # contour - get the contour from the mask
        img_in, cntr, contours, edges = drawContour(img_in,a3,False,100,1,1,60,240,30,7)
        #contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    #    print(len(contours[0]))
    #     contours[0] = contours[0][:(len(contours[0])//2)]
        fourier_desc = None
        img_fd = None
        fourier_desc = findDescriptor(contours)
        if len(fourier_desc)>0:
            img_fd, fourier_desc = reconstruct(fourier_desc, 80, IMG_SIZE)
            fourier_desc = truncate_descriptor(fourier_desc,10)
    
        # find and enpasise edges
        kernel = np.array([[0.5, 1.0, 0.5], 
                       [1.0, -6.0, 1.0],
                       [0.5, 1.0, 0.5]])
        kernel = kernel/(np.sum(kernel) if np.sum(kernel)!=0 else 1)
        #filter the source img_in
        #img_in = cv2.filter2D(img_in,-1,kernel)
    
        #img_in = (255-img_in) # inverse
        # resized, feature enhanced, mask, contour
    except:
        return None, None, None, None, None, None, 2
    return img_rsz, img_in, a3, cntr, img_fd, fourier_desc, 0