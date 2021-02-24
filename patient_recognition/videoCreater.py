import numpy as np
import cv2
import glob
 
img_array = []
for i in range(1300):
    # print(i)
    img = cv2.imread("{}.png".format(i))
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('patientDetectionDemo.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()