import numpy as np
# from fnc.boundary import searchInnerBound, searchOuterBound
# from fnc.line import findline, linecoords
import multiprocessing as mp
import cv2
from matplotlib import pyplot as plt
import multiprocessing as mp
from .linecoords import linecoords
from .findline import findline
from .search_inner_bound import search_inner_bound
from .search_outer_bound import search_outer_bound


def segment(eyeimage, eyelashes_thres=80, use_multiprocess=False):
	"""
	Description:
		Segment the iris region from the eye image.
		Indicate the noise region.

	Input:
		eyeimage:			Eye image
		eyelashes_thres:   	Eyelashes threshold
		use_multiprocess:   	Use multiprocess to run

	Output:
		circleiris:		Centre coordinates and radius of iris boundary.
		circlepupil:	Centre coordinates and radius of pupil boundary.
		imagewithnoise:	Original image but with location of noise marked with NaN.
	"""
	# print("segment")
	# Find the iris boundary by Daugman's intefro-differential
	rowp, colp, rp = search_inner_bound(eyeimage)
	row, col, r = search_outer_bound(eyeimage, rowp, colp, rp)

	# Package pupil and iris boundaries
	rowp = np.round(rowp).astype(int)
	colp = np.round(colp).astype(int)
	rp = np.round(rp).astype(int)

	row = np.round(row).astype(int)
	col = np.round(col).astype(int)
	r = np.round(r).astype(int)

	circlepupil = [rowp, colp, rp]
	circleiris = [row, col, r]

	# Find top and bottom eyelid
	imsz = eyeimage.shape
	irl = np.round(row - r).astype(int)
	iru = np.round(row + r).astype(int)
	icl = np.round(col - r).astype(int)
	icu = np.round(col + r).astype(int)
	if irl < 0:
		irl = 0
	if icl < 0:
		icl = 0
	if iru >= imsz[0]:
		iru = imsz[0] - 1
	if icu >= imsz[1]:
		icu = imsz[1] - 1
	imageiris = eyeimage[irl: iru + 1, icl: icu + 1]

	# If use_multiprocess
	if use_multiprocess:
		ret_top = mp.Manager().dict()
		ret_bot = mp.Manager().dict()
		p_top = mp.Process(
			target=find_top_eyelid,
			args=(imsz, imageiris, irl, icl, rowp, rp, ret_top),
		)
		p_bot = mp.Process(
			target=find_bottom_eyelid,
			args=(imsz, imageiris, rowp, rp, irl, icl, ret_bot),
		)
		p_top.start()
		p_bot.start()
		p_top.join()
		p_bot.join()
		mask_top = ret_top[0]
		mask_bot = ret_bot[0]

	# If not use_multiprocess
	else:
		mask_top = find_top_eyelid(imsz, imageiris, irl, icl, rowp, rp)
		mask_bot = find_bottom_eyelid(imsz, imageiris, rowp, rp, irl, icl)

	# Mask the eye image, noise region is masked by NaN value
	imagewithnoise = eyeimage.astype(float)
	imagewithnoise = imagewithnoise + mask_top + mask_bot

	# For CASIA, eliminate eyelashes by threshold
	ref = eyeimage < eyelashes_thres
	coords = np.where(ref == 1)
	imagewithnoise[tuple(coords)] = np.nan

	# print("----SEGMENT", circleiris, circlepupil)
	return circleiris, circlepupil, imagewithnoise

#------------------------------------------------------------------------------
#               METHODS USED FOR MULTIPROCESSOR
#------------------------------------------------------------------------------
def find_top_eyelid(imsz, imageiris, irl, icl, rowp, rp, ret_top=None):
	"""
	Description:
		Mask for the top eyelid region.

	Input:
		imsz:		Size of the eye image.
		imageiris:	Image of the iris region.
		irl:		iris low
		icl:		iris
		rowp:		y-coordinate of the inner circle centre.
		rp:			radius of the inner circle centre.
		ret_top:	Just used for returning result when using multiprocess.

	Output:
		mask:		Map of noise that will be masked with NaN values.
	"""
	# print("find_top_eyelid")
	topeyelid = imageiris[0: rowp - irl - rp, :]
	lines = findline(topeyelid)
	mask = np.zeros(imsz, dtype=float)

	if lines.size > 0:
		xl, yl = linecoords(lines, topeyelid.shape)
		yl = np.round(yl + irl - 1).astype(int)
		xl = np.round(xl + icl - 1).astype(int)

		yla = np.max(yl)
		y2 = np.arange(yla)

		mask[yl, xl] = np.nan
		grid = np.meshgrid(y2, xl)
		mask[tuple(grid)] = np.nan

	# Return
	if ret_top is not None:
		ret_top[0] = mask
	return mask


#------------------------------------------------------------------------------
def find_bottom_eyelid(imsz, imageiris, rowp, rp, irl, icl, ret_bot=None):
	"""
	Description:
		Mask for the bottom eyelid region.

	Input:
		imsz:		Eye image.
		imageiris:	Image of the iris region.
		rowp:		y-coordinate of the inner circle centre.
		rp:			radius of the inner circle centre.
		ret_bot:	Just used for returning result when using multiprocess.

	Output:
		mask:		Map of noise that will be masked with NaN values.
	"""
	# print("find_bottom_eyelid")
	bottomeyelid = imageiris[rowp - irl + rp - 1 : imageiris.shape[0], :]
	lines = findline(bottomeyelid)
	mask = np.zeros(imsz, dtype=float)

	if lines.size > 0:
		xl, yl = linecoords(lines, bottomeyelid.shape)
		yl = np.round(yl + rowp + rp - 3).astype(int)
		xl = np.round(xl + icl - 2).astype(int)
		yla = np.min(yl)
		y2 = np.arange(yla-1, imsz[0])

		mask[yl, xl] = np.nan
		grid = np.meshgrid(y2, xl)
		mask[tuple(grid)] = np.nan

	# Return
	if ret_bot is not None:
		ret_bot[0] = mask
	return mask