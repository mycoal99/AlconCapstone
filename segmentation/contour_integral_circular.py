import cv2
import numpy as np

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

