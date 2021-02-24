import cv2
import numpy as np

def shiftbits(template, noshifts):
	"""
	Description:
		Shift the bit-wise iris patterns.

	Input:
		template	- The template to be shifted.
		noshifts	- The number of shift operators, positive for right
					  direction and negative for left direction.

	Output:
		templatenew	- The shifted template.
	"""
	# print("shiftbits")
	# Initialize
	templatenew = np.zeros(template.shape)
	width = template.shape[1]
	s = 2 * np.abs(noshifts)
	p = width - s

	# Shift
	if noshifts == 0:
		templatenew = template

	elif noshifts < 0:
		x = np.arange(p)
		templatenew[:, x] = template[:, s + x]
		x = np.arange(p, width)
		templatenew[:, x] = template[:, x - p]

	else:
		x = np.arange(s, width)
		templatenew[:, x] = template[:, x - s]
		x = np.arange(s)
		templatenew[:, x] = template[:, p + x]

	# Return
	return templatenew
