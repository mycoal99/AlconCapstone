import numpy as np

def adjgamma(im, g):
    """
	Description:
		Adjust image gamma.

	Input:
		im:     The input image.
		g:      Image gamma value.
				  Range (0, 1] enhances contrast of bright region.
				  Range (1, inf) enhances contrast of dark region.

	Output:
		newim   - The adjusted image.
	"""
    if g <= 0:
        raise Exception("adjgamma.py >>> Gamma value must be > 0")
    # print("adjgamma")
    newim = im
    newim = newim - np.min(newim)
    newim = newim / np.max(newim)
    newim = newim ** (1 / g)  # Apply gamma function
    # cv2.imwrite("original.png", im)
    # cv2.imwrite("adjustgamma.png",newim)
    return newim

