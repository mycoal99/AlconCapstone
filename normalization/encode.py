import cv2
import numpy as np
from .gaborconvolve import gaborconvolve


def encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf):
	"""
	Description:
		Generate iris template and noise mask from the normalised iris region.

	Input:
		polar_array		- Normalised iris region.
		noise_array		- Normalised noise region.
		minWaveLength	- Base wavelength.
		mult			- Multicative factor between each filter.
		sigmaOnf		- Bandwidth parameter.

	Output:
		template		- The binary iris biometric template.
		mask			- The binary iris noise mask.
	"""
	# Convolve normalised region with Gabor filters
	filterbank = gaborconvolve(polar_array, minWaveLength, mult, sigmaOnf)

	length = polar_array.shape[1]
	template = np.zeros([polar_array.shape[0], 2 * length])
	h = np.arange(polar_array.shape[0])

	# Create the iris template
	mask = np.zeros(template.shape)
	eleFilt = filterbank[:, :]

	# Phase quantization
	H1 = np.real(eleFilt) > 0
	H2 = np.imag(eleFilt) > 0

	# If amplitude is close to zero then phase data is not useful,
	# so mark off in the noise mask
	H3 = np.abs(eleFilt) < 0.0001
	for i in range(length):
		ja = 2 * i

		# Construct the biometric template
		template[:, ja] = H1[:, i]
		template[:, ja + 1] = H2[:, i]

		# Create noise mask
		mask[:, ja] = noise_array[:, i] | H3[:, i]
		mask[:, ja + 1] = noise_array[:, i] | H3[:, i]

	# Return
	return template, mask
