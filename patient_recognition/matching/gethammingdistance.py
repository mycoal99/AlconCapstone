import cv2
import numpy as np
from .shiftbits import shiftbits


def gethammingdistance(template1, mask1, template2, mask2):
	"""
	Description:
		Calculate the Hamming distance between two iris templates.

	Input:
		template1	- The first template.
		mask1		- The first noise mask.
		template2	- The second template.
		mask2		- The second noise mask.

	Output:
		hd			- The Hamming distance as a ratio.
	"""
	# print("calHammingDist")
	# Initialize
	hd = np.nan

	# Shift template left and right, use the lowest Hamming distance
	for shifts in range(-8,9):
		template1s = shiftbits(template1, shifts)
		mask1s = shiftbits(mask1, shifts)

		mask = np.logical_or(mask1s, mask2)
		nummaskbits = np.sum(mask==1)
		totalbits = template1s.size - nummaskbits

		C = np.logical_xor(template1s, template2)
		C = np.logical_and(C, np.logical_not(mask))
		bitsdiff = np.sum(C==1)

		if totalbits==0:
			hd = np.nan
		else:
			hd1 = bitsdiff / totalbits
			if hd1 < hd or np.isnan(hd):
				hd = hd1

	# Return
	return hd