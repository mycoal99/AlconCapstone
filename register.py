##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os, sys
from time import time
from scipy.io import savemat
import cv2
from segmentation.segmentiris import segment
from normalization.normalizeiris import normalizeiris
from normalization.encode import encode
import patient_db
import hashlib
import json

### SET UP DATABASE PATH-----------------------------------------------------------
with open('db-config.json') as f:
    config = json.load(f)


PATH = config['database-local-path']
DATABASE_NAME = config['database-name']
EYE_TEMPLATE_PATH = config['eye-template-folder-name']

try:
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    try:
        if not os.path.exists(PATH + '/' + EYE_TEMPLATE_PATH):
            os.makedirs(PATH + '/' + EYE_TEMPLATE_PATH)
    except:
        print("[EXCEPTION]: eye-template directory path is not valid.")
except:
    print("[EXCEPTION]: database directory path is not valid.")



DATABASE_NAME = PATH + '/' + DATABASE_NAME

### -----------------------------------------------------------------------------------

# from fnc.extractFeature import extractFeature
# Segmentation parameters
eyelashes_thres = 80

# Normalisation parameters
radial_res = 20
angular_res = 240

# Feature encoding parameters
minWaveLength = 18
mult = 1
sigmaOnf = 0.5


#------------------------------------------------------------------------------
#	Argument parsing
#------------------------------------------------------------------------------
_, left, right = sys.argv
print(left, "-----", right)
use_multiprocess = False

# getting features
try:
    img = cv2.imread(left, 0)
except:
    raise Exception("File not found.")

circleiris, circlepupil, imwithnoise = segment(img, eyelashes_thres, use_multiprocess)
polar_array, noise_array = normalizeiris(imwithnoise, circleiris[1], circleiris[0], circleiris[2],
										 circlepupil[1], circlepupil[0], circlepupil[2],
										 radial_res, angular_res)

template, mask = encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf)


### ADD TO DATABASE
patient_id = "1"
firstname = "Brent"
lastname = "Luker"
DOB = "09/20/1999"
left_eye_template = left
right_eye_template = right
surgery = "cataract-surgery"
left_eye_template = hashlib.sha512(left_eye_template.encode()).hexdigest() 
right_eye_template = hashlib.sha512(right_eye_template.encode()).hexdigest() 
print(left_eye_template)
print(right_eye_template)
patient_db.add_patient(firstname, lastname, DOB, left_eye_template, right_eye_template, surgery)



# Save extracted feature
basename = os.path.basename(left_eye_template)
out_file = os.path.join(PATH + '/' + EYE_TEMPLATE_PATH, "%s.mat" % (basename))
savemat(out_file, mdict={'template':template, 'mask':mask})





# -------------RIGHT
# getting features
try:
    img = cv2.imread(right, 0)
except:
    raise Exception("File not found.")

circleiris, circlepupil, imwithnoise = segment(img, eyelashes_thres, use_multiprocess)
polar_array, noise_array = normalizeiris(imwithnoise, circleiris[1], circleiris[0], circleiris[2],
										 circlepupil[1], circlepupil[0], circlepupil[2],
										 radial_res, angular_res)

template, mask = encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf)




# Save extracted feature
basename = os.path.basename(right_eye_template)
out_file = os.path.join(PATH + '/' + EYE_TEMPLATE_PATH, "%s.mat" % (basename))
savemat(out_file, mdict={'template':template, 'mask':mask})








# print(out_file)
##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
# start = time()
# # args.file = "../CASIA1/001_1_1.jpg"

# # Extract feature
# print('>>> Enroll for the file ', args.file)
# template, mask, file = extractFeature(args.file)

# # Save extracted feature
# basename = os.path.basename(file)
# out_file = os.path.join(args.temp_dir, "%s.mat" % (basename))
# savemat(out_file, mdict={'template':template, 'mask':mask})
# print('>>> Template is saved in %s' % (out_file))

# end = time()
# print('>>> Enrollment time: {} [s]\n'.format(end-start))