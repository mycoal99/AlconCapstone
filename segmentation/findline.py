import cv2
import numpy as np
from scipy.ndimage import convolve
from skimage.transform import radon
from .canny import canny
from .adjgamma import adjgamma
from .nonmaxsup import nonmaxsup
from .hysthresh import hysthresh

def findline(img):
    """
	Description:
		Find lines in an image.
		Linear Hough transform and Canny edge detection are used.

	Input:
		img:    The input image.

	Output:
		lines:  Parameters of the detected line in polar form. (r, theta)
	"""
    # print("findline")
    # Pre-processing
    I2, orient = canny(img, 2, 0, 1)
    # cv2.imwrite("I2.png", I2)
    I3 = adjgamma(I2, 1.9)
    I4 = nonmaxsup(I3, orient, 1.5)
    edgeimage = hysthresh(I4, 0.2, 0.15)

    # Radon transformation
    theta = np.arange(180)
    R = radon(edgeimage, theta, circle=False)
    sz = R.shape[0] // 2
    xp = np.arange(-sz, sz+1, 1)

    # Find for the strongest edge
    maxv = np.max(R)
    if maxv > 25:
        i = np.where(R.ravel() == maxv)
        i = i[0]
    else:
        return np.array([])

    R_vect = R.ravel()
    ind = np.argsort(-R_vect[i])
    u = i.shape[0]
    k = i[ind[0: u]]
    y, x = np.unravel_index(k, R.shape)
    t = -theta[x] * np.pi / 180
    r = xp[y]

    lines = np.vstack([np.cos(t), np.sin(t), -r]).transpose()
    cx = img.shape[1] / 2 - 1
    cy = img.shape[0] / 2 - 1
    lines[:, 2] = lines[:,2] - lines[:,0]*cx - lines[:,1]*cy
    return lines

