import argparse
import cv2
from time import time
from matching.matching import matching
import sys
from segmentation.segmentiris import segment
from normalization.normalizeiris import normalizeiris
from normalization.encode import encode
import patient_db
import json

### SET UP DATABASE PATH-----------------------------------------------------------
with open('db-config.json') as f:
    config = json.load(f)


PATH = config['database-local-path']
DATABASE_NAME = config['database-name']
EYE_TEMPLATE_PATH = config['eye-template-folder-name']
### -------------------------------------------------------------------------------


# # Segmentation parameters
# eyelashes_thres = 80

# # Normalisation parameters
# radial_res = 20
# angular_res = 240

# # Feature encoding parameters
# minWaveLength = 18
# mult = 1
# sigmaOnf = 0.5
#------------------------------------------------

# _, filename = sys.argv
# print(filename)
# use_multiprocess = False

# # getting features
# try:
#     img = cv2.imread(filename, 0)
# except:
#     raise Exception("File not found.")


# circleiris, circlepupil, imwithnoise = segment(img, eyelashes_thres, use_multiprocess)
# polar_array, noise_array = normalize(imwithnoise, circleiris[1], circleiris[0], circleiris[2],
# 										 circlepupil[1], circlepupil[0], circlepupil[2],
# 										 radial_res, angular_res)

# template, mask = encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf)

# if __name__=="__main__":
#     temp_dir = "./diagnostics/"
#     threshold = 0.38

#     result = matching(template, mask, temp_dir, threshold)

#     if result == -1:
#         print('>>> No registered sample.')

#     elif result == 0:
#         print('>>> No sample matched.')

#     else:
#         print('>>> {} samples matched (descending reliability):'.format(len(result)))
#         for res in result:
#             print("\t", res)
#             eye_template = res.split(".")[0]
#             patient_db.get_patient_by_eye_template(eye_template)


# ------------------------------------------------------------------------------------------

def verify(img):
    """
        Input:
            img: image to be verified
        
        Output:
            


    """

    # Segmentation parameters
    eyelashes_thres = 80

    # Normalisation parameters
    radial_res = 20
    angular_res = 240

    # Feature encoding parameters
    minWaveLength = 18
    mult = 1
    sigmaOnf = 0.5
    use_multiprocess = True

    circleiris, circlepupil, imwithnoise = segment(img, eyelashes_thres, use_multiprocess)
    polar_array, noise_array = normalizeiris(imwithnoise, circleiris[1], circleiris[0], circleiris[2],
                                            circlepupil[1], circlepupil[0], circlepupil[2],
                                            radial_res, angular_res)

    template, mask = encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf)

    temp_dir = PATH + '/' + EYE_TEMPLATE_PATH
    threshold = 0.38

    result = matching(template, mask, temp_dir, threshold)

    if result == -1:
        print('>>> No registered template.')

    elif result == 0:
        print('>>> No template matched.')

    else:
        print('>>>[PATIENT FOUND] {} template(s) matched:'.format(len(result)))
        for res in result:
            print("\t", res)
            eye_template = res.split(".")[0]
            print(patient_db.get_patient_by_left_eye_template(eye_template))
            print(patient_db.get_patient_by_right_eye_template(eye_template))


