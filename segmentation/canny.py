import cv2
import numpy as np
from scipy.ndimage import convolve
from skimage.transform import radon


def canny(im, sigma, vert, horz):
    """
	Description:
		Canny edge detection.

	Input:
		im:     The input image.
		sigma:  Standard deviation of Gaussian smoothing filter.
		vert:   Weighting for vertical gradients.
		horz:   Weighting for horizontal gradients.

	Output:
		grad:   Edge strength (gradient amplititude)
		orient: Orientation image (0-180, positive, anti-clockwise)
	"""
    # print("canny")
    xscaling = vert
    yscaling = horz
    hsize = [6 * sigma + 1, 6 * sigma + 1]  # The filter size



    def fspecial_gaussian(shape=(3, 3), sig=1):
        # print("fspecial_gaussian")
        m, n = [(ss - 1) / 2 for ss in shape]
        y, x = np.ogrid[-m:m + 1, -n:n + 1]
        f = np.exp(-(x * x + y * y) / (2 * sig * sig))
        f[f < np.finfo(f.dtype).eps * f.max()] = 0
        sum_f = f.sum()
        if sum_f != 0:
            f /= sum_f
        return f

    
    gaussian = fspecial_gaussian(hsize, sigma)
    im = convolve(im, gaussian, mode='constant')  # Smoothed image
    rows, cols = im.shape

    h = np.concatenate([im[:, 1:cols], np.zeros([rows,1])], axis=1) - \
        np.concatenate([np.zeros([rows, 1]), im[:, 0: cols - 1]], axis=1)

    v = np.concatenate([im[1: rows, :], np.zeros([1, cols])], axis=0) - \
        np.concatenate([np.zeros([1, cols]), im[0: rows - 1, :]], axis=0)

    d11 = np.concatenate([im[1:rows, 1:cols], np.zeros([rows - 1, 1])], axis=1)
    d11 = np.concatenate([d11, np.zeros([1, cols])], axis=0)
    d12 = np.concatenate([np.zeros([rows-1, 1]), im[0:rows - 1, 0:cols - 1]], axis=1)
    d12 = np.concatenate([np.zeros([1, cols]), d12], axis=0)
    d1 = d11 - d12

    d21 = np.concatenate([im[0:rows - 1, 1:cols], np.zeros([rows - 1, 1])], axis=1)
    d21 = np.concatenate([np.zeros([1, cols]), d21], axis=0)
    d22 = np.concatenate([np.zeros([rows - 1, 1]), im[1:rows, 0:cols - 1]], axis=1)
    d22 = np.concatenate([d22, np.zeros([1, cols])], axis=0)
    d2 = d21 - d22

    X = (h + (d1 + d2) / 2) * xscaling
    Y = (v + (d1 - d2) / 2) * yscaling

    gradient = np.sqrt(X * X + Y * Y)  # Gradient amplitude

    orient = np.arctan2(-Y, X)  # Angles -pi to +pi
    neg = orient < 0  # Map angles to 0-pi
    orient = orient * ~neg + (orient + np.pi) * neg
    orient = orient * 180 / np.pi  # Convert to degrees

    return gradient, orient
