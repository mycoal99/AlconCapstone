##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import numpy as np
from os import listdir
from fnmatch import filter
import scipy.io as sio
from multiprocessing import Pool, cpu_count, freeze_support
from itertools import repeat
from .gethammingdistance import gethammingdistance

import warnings
warnings.filterwarnings("ignore")

# print("MATCHING")
##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
def matching(template_extr, mask_extr, temp_dir, threshold=0.38):
	"""
	Description:
		Match the extracted template with database.

	Input:
		template_extr	- Extracted template.
		mask_extr		- Extracted mask.
		threshold		- Threshold of distance.
		temp_dir		- Directory contains templates.

	Output:
		List of strings of matched files, 0 if not, -1 if no registered sample.
	"""
	# print("matching")
	# Get the number of accounts in the database
	n_files = len(filter(listdir(temp_dir), '*.mat'))
	# print("-------nfiles:", n_files)
	if n_files == 0:
		return -1

	# Use all cores to calculate Hamming distances
	args = zip(
		sorted(listdir(temp_dir)),
		repeat(template_extr),
		repeat(mask_extr),
		repeat(temp_dir),
	)
	
	with Pool(processes=cpu_count()) as pools:
		result_list = pools.starmap(matchingPool, args)

	filenames = [result_list[i][0] for i in range(len(result_list))]
	hm_dists = np.array([result_list[i][1] for i in range(len(result_list))])

	# Remove NaN elements
	ind_valid = np.where(hm_dists>0)[0]
	hm_dists = hm_dists[ind_valid]
	filenames = [filenames[idx] for idx in ind_valid]

	# Threshold and give the result ID
	ind_thres = np.where(hm_dists<=threshold)[0]

	# Return
	if len(ind_thres)==0:
		return 0
	else:
		hm_dists = hm_dists[ind_thres]
		filenames = [filenames[idx] for idx in ind_thres]
		ind_sort = np.argsort(hm_dists)
		return [filenames[idx] for idx in ind_sort]




def matchingPool(file_temp_name, template_extr, mask_extr, temp_dir):
	"""
	Description:
		Perform matching session within a Pool of parallel computation

	Input:
		file_temp_name	- File name of the examining template
		template_extr	- Extracted template
		mask_extr		- Extracted mask of noise

	Output:
		hm_dist			- Hamming distance
	"""
	# print("matchingPool")
	# Load each account
	data_template = sio.loadmat('%s%s'% (temp_dir, file_temp_name))
	template = data_template['template']
	mask = data_template['mask']

	# Calculate the Hamming distance
	hm_dist = gethammingdistance(template_extr, mask_extr, template, mask)
	return (file_temp_name, hm_dist)