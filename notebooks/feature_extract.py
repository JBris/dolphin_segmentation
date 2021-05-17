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

def contrast_yt(img,a=0,b=0,c=255):
    yt = threshold_yen(img)
    img = rescale_intensity(img, (a, yt/2), (b, c))
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

def drawContour(img,mask,smooth=True,sv=100,d=8,de=6, ka=50, kb=50, kc=5, kk=3):
    cntr = np.zeros(mask.shape, np.uint8)
    # Use Canny to detect edges
    edges = cv2.Canny(mask, ka, kb, kc)
    # Dilate and erode to thicken the edges
    kernel = np.ones((kk, kk), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations = de)
    edges = cv2.erode(edges, kernel, iterations = de)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # CHAIN_APPROX_SIMPLE CHAIN_APPROX_NONE  
    
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
        cv2.drawContours(img, smoothened, -1, (0,0,0), d)
    else:
        cv2.drawContours(img, contours, -1, (0,0,0), d)
    cv2.drawContours(cntr, contours, -1, (255,255,255), d)    
    return img, cntr, contours


##################################################################
## Fourier-Descriptor 

def findDescriptor(contour):
    # finds and returns the Fourier-Descriptor of the contour
    contour_array = contour[0][:, 0, :]
    contour_complex = np.empty(contour_array.shape[:-1], dtype=complex)
    contour_complex.real = contour_array[:, 0]
    contour_complex.imag = contour_array[:, 1]
    fourier_result = np.fft.fft(contour_complex)
    return fourier_result

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