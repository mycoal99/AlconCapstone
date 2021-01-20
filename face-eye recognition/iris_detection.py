import numpy as np
import cv2
import math
import string
from scipy import signal
from .contour_integral_circular import contour_integral_circular
'''
    Assumptions:
        - one specified eye is in frame
        - no zooming or cropping of the image
        - only moving the robot arm
'''
def contour_integral_circular(imagen, y0, x0, r, angs):
   """
   Description:
       Performs contour circular integral using discrete Rie-mann approach.
 
   Input:
       imagen: The input iris image.
       y0:     The y-coordinate of the circle center.
       x0:     The x-coordinate of the circle center.
       r:      The radius of the circle.
       angs:   integration angles clockwise 0-2pi.
 
   Output:
       hs:     Hough space result (from integration)
   """
 
   # Get y, x
   y = np.zeros([len(angs), r.shape[0], r.shape[1], r.shape[2]], dtype=int)
   x = np.zeros([len(angs), r.shape[0], r.shape[1], r.shape[2]], dtype=int)
   for i in range(len(angs)):
       ang = angs[i]
       y[i, :, :, :] = np.round(y0 - np.cos(ang) * r).astype(int)
       x[i, :, :, :] = np.round(x0 + np.sin(ang) * r).astype(int)
 
   # Adapt y
   ind = np.where(y < 0)
   y[ind] = 0
   ind = np.where(y >= imagen.shape[0])
   y[ind] = imagen.shape[0] - 1
 
   # Adapt x
   ind = np.where(x < 0)
   x[ind] = 0
   ind = np.where(x >= imagen.shape[1])
   x[ind] = imagen.shape[1] - 1
 
   # Return
   hs = imagen[y, x]
   hs = np.sum(hs, axis=0)
   return hs.astype(float)

def search_inner_bound(img):
   """
   Description:
       Search for the inner boundary of the iris.
 
   Input:
       img:    The input iris image.
 
   Output:
       inner_y:    y-coordinate of the inner circle centre.
       inner_x:    x-coordinate of the inner circle centre.
       inner_r:    Radius of the inner circle.
   """
   # print("---searchInnerBound")
 
   # Integro-Differential operator coarse (jump-level precision)
   Y = img.shape[0]
   X = img.shape[1]
   sect = X/4      # Width of the external marg in for which search is excluded
   minrad = 10
   maxrad = sect*0.8
   jump = 4        # Precision of the coarse search, in pixels
 
   # Hough Space (y,x,r)
   sz = np.array([np.floor((Y-2*sect)/jump),
                   np.floor((X-2*sect)/jump),
                   np.floor((maxrad-minrad)/jump)]).astype(int)
 
   # Resolution of the circular integration
   integrationprecision = 1
   angs = np.arange(0, 2*np.pi, integrationprecision)
   x, y, r = np.meshgrid(np.arange(sz[1]),
                         np.arange(sz[0]),
                         np.arange(sz[2]))
   y = sect + y*jump
   x = sect + x*jump
   r = minrad + r*jump
   hs = contour_integral_circular(img, y, x, r, angs)
 
   # Hough Space Partial Derivative R
   hspdr = hs - hs[:, :, np.insert(np.arange(hs.shape[2]-1), 0, 0)]
 
   # Blur
   sm = 3      # Size of the blurring mask
   hspdrs = signal.fftconvolve(hspdr, np.ones([sm,sm,sm]), mode="same")
 
   indmax = np.argmax(hspdrs.ravel())
   y,x,r = np.unravel_index(indmax, hspdrs.shape)
 
 
   inner_y = sect + y*jump
   inner_x = sect + x*jump
   inner_r = minrad + (r-1)*jump
 
   # Integro-Differential operator fine (pixel-level precision)
   integrationprecision = 0.1      # Resolution of the circular integration
   angs = np.arange(0, 2*np.pi, integrationprecision)
   x, y, r = np.meshgrid(np.arange(jump*2),
                         np.arange(jump*2),
                         np.arange(jump*2))
   y = inner_y - jump + y
   x = inner_x - jump + x
   r = inner_r - jump + r
   hs = contour_integral_circular(img, y, x, r, angs)
 
   # Hough Space Partial Derivative R
   hspdr = hs - hs[:, :, np.insert(np.arange(hs.shape[2]-1), 0, 0)]
 
   # Bluring
   sm = 3      # Size of the blurring mask
   hspdrs = signal.fftconvolve(hspdr, np.ones([sm,sm,sm]), mode="same")
   indmax = np.argmax(hspdrs.ravel())
   y,x,r = np.unravel_index(indmax, hspdrs.shape)
 
   inner_y = inner_y - jump + y
   inner_x = inner_x - jump + x
   inner_r = inner_r - jump + r - 1
   # print("INNERBOUND:", inner_y, inner_x, inner_r)
   return inner_y, inner_x, inner_r


#set surgical camera as videoSource
VIDEO_SOURCE = 0
SET_UP_COMPLETE = False

#begin live stream
cap = cv2.VideoCapture(VIDEO_SOURCE) 
ret, img = cap.read()
height, width, channels = img.shape

try:
    while not SET_UP_COMPLETE:
        ret, img = cap.read()
        rows, cols, _ = img.shape 

        #Iris and Pupil detection
        search_inner_bound(img)

        #move robot to center eye
        

        #move robot to closer to eye




'''
    Assumptions:
        - two eyes is in frame
'''