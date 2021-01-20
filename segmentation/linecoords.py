import cv2
import numpy as np

def linecoords(lines, imsize):
    """
	Description:
		Find x-, y- coordinates of positions along a line.

	Input:
		lines:  Parameters (polar form) of the line.
		imsize: Size of the image.

	Output:
		x,y:    Resulting coordinates.
	"""
    # print("linecoords")
    xd = np.arange(imsize[1])
    yd = (-lines[0,2] - lines[0,0] * xd) / lines[0,1]

    coords = np.where(yd >= imsize[0])
    coords = coords[0]
    yd[coords] = imsize[0]-1
    coords = np.where(yd < 0)
    coords = coords[0]
    yd[coords] = 0

    x = xd
    y = yd
    return x, y
