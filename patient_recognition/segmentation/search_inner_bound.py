##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np
from scipy import signal
from .contour_integral_circular import contour_integral_circular


# print("BOUNDARY")
##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
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
    sect = X/4 		# Width of the external marg in for which search is excluded
    minrad = 10
    maxrad = sect*0.8
    jump = 4 		# Precision of the coarse search, in pixels

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
    sm = 3 		# Size of the blurring mask
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>", hspdr, hspdr.shape)
    hspdrs = signal.fftconvolve(hspdr, np.ones([sm,sm,sm]), mode="same")

    indmax = np.argmax(hspdrs.ravel())
    y,x,r = np.unravel_index(indmax, hspdrs.shape)


    inner_y = sect + y*jump
    inner_x = sect + x*jump
    inner_r = minrad + (r-1)*jump

    # Integro-Differential operator fine (pixel-level precision)
    integrationprecision = 0.1 		# Resolution of the circular integration
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
    sm = 3 		# Size of the blurring mask
    hspdrs = signal.fftconvolve(hspdr, np.ones([sm,sm,sm]), mode="same")
    indmax = np.argmax(hspdrs.ravel())
    y,x,r = np.unravel_index(indmax, hspdrs.shape)

    inner_y = inner_y - jump + y
    inner_x = inner_x - jump + x
    inner_r = inner_r - jump + r - 1
    # print("INNERBOUND:", inner_y, inner_x, inner_r)
    return inner_y, inner_x, inner_r

