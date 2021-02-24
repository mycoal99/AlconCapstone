import cv2
import numpy as np
from scipy.ndimage import convolve
from skimage.transform import radon

def nonmaxsup(in_img, orient, radius):
    """
    Description:
        Perform non-maxima suppression on an image using an orientation image

    Input:
        in_img: The input image
        orient: Image containing feature normal orientation angles
        radius: Distance to be looked at on each side of each pixel when
                  determining whether it is a local maxima or not (1.2 - 1.5)

    Output:
        im_out: The suppressed image
    """
    # print("nonmaxsup")
    # Preallocate memory for output image for speed
    rows, cols = in_img.shape
    im_out = np.zeros([rows, cols])
    iradius = np.ceil(radius).astype(int)

    # Pre-calculate x and y offsets relative to centre pixel for each orientation angle
    angle = np.arange(181) * np.pi / 180  # Angles in 1 degree increments (in radians)
    xoff = radius * np.cos(angle)  # x and y offset of points at specified radius and angle
    yoff = radius * np.sin(angle)  # from each reference position

    hfrac = xoff - np.floor(xoff)  # Fractional offset of xoff relative to integer location
    vfrac = yoff - np.floor(yoff)  # Fractional offset of yoff relative to integer location

    orient = np.fix(orient)

    # Now run through the image interpolating grey values on each side
    # of the centre pixel to be used for the non-maximal suppression
    col, row = np.meshgrid(np.arange(iradius, cols - iradius),
                           np.arange(iradius, rows - iradius))

    # Index into precomputed arrays
    ori = orient[row, col].astype(int)

    # x, y location on one side of the point in question
    x = col + xoff[ori]
    y = row - yoff[ori]

    # Get integer pixel locations that surround location x,y
    fx = np.floor(x).astype(int)
    cx = np.ceil(x).astype(int)
    fy = np.floor(y).astype(int)
    cy = np.ceil(y).astype(int)

    # Value at integer pixel locations
    tl = in_img[fy, fx]  # top left
    tr = in_img[fy, cx]  # top right
    bl = in_img[cy, fx]  # bottom left
    br = in_img[cy, cx]  # bottom right

    # Bi-linear interpolation to estimate value at x,y
    upperavg = tl + hfrac[ori] * (tr - tl)
    loweravg = bl + hfrac[ori] * (br - bl)
    v1 = upperavg + vfrac[ori] * (loweravg - upperavg)

    # Check the value on the other side
    map_candidate_region = in_img[row, col] > v1

    x = col - xoff[ori]
    y = row + yoff[ori]

    fx = np.floor(x).astype(int)
    cx = np.ceil(x).astype(int)
    fy = np.floor(y).astype(int)
    cy = np.ceil(y).astype(int)

    tl = in_img[fy, fx]
    tr = in_img[fy, cx]
    bl = in_img[cy, fx]
    br = in_img[cy, cx]

    upperavg = tl + hfrac[ori] * (tr - tl)
    loweravg = bl + hfrac[ori] * (br - bl)
    v2 = upperavg + vfrac[ori] * (loweravg - upperavg)

    # Local maximum
    map_active = in_img[row, col] > v2
    map_active = map_active * map_candidate_region
    im_out[row, col] = in_img[row, col] * map_active

    return im_out
