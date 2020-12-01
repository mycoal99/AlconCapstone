import numpy as np
import cv2
import math
from facenet_webcam import FaceDetector
from facenet_webcam import MTCNN
import sys
import string

#run Patient detection
mtcnn = MTCNN()
fd = FaceDetector(mtcnn)
# change 0 to args[0] or pass in video streamer
videoSource = fd.videoSources["native"] #NEED TO CHANGE
patient = fd.start(videoSource)
print(patient)
#save coordinates of patient's eyes
eyes = [patient[0], patient[1]]

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#start video to detect eye and zoom into setup possible
cap = cv2.VideoCapture(0) 
ret, img = cap.read()
height, width, channels = img.shape

videoWriter = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('X','V','I','D'), 10, (width,height))

#display patient with boxes around eyes
i = 0
while i < 30:
    ret, img = cap.read()
    boxed_img = img
    #drawing red boxes around the patients eyes
    pt1 = (int(eyes[0][0] - 35), int(eyes[0][1] - 35))
    pt2 = (int(eyes[0][0] + 35) , int(eyes[0][1] + 35))
    #draw box around right eye and add text 'Right'
    cv2.rectangle(boxed_img, pt1, pt2, color=(0, 0, 255), thickness=2)
    font = cv2.FONT_HERSHEY_SIMPLEX 
    cv2.putText(boxed_img, 'Right', (pt1[0],  pt1[1] + 100), font, 1, (0, 0, 255), 2, cv2.LINE_4)

    pt1 = (int(eyes[1][0] - 35), int(eyes[1][1] - 35))
    pt2 = (int(eyes[1][0] + 35) , int(eyes[1][1] + 35))
    #draw box around left eye and add text 'Left'
    cv2.rectangle(boxed_img, pt1, pt2, color=(0, 0, 255), thickness=2)
    cv2.putText(boxed_img,  'Left', (pt1[0],  pt1[1] + 100), font, 1, (0, 0, 255), 2, cv2.LINE_4)

    cv2.imshow('Patient Eyes', boxed_img)
    cv2.waitKey(30)
    i += 1

cv2.destroyAllWindows()

# prompting user to input r or l to select eye
eye = patient[0]
var = input("Enter right(r) or left(l) eye: ")
while(var != 'r' and var != 'l'):
    if(var == "right"):
        var = 'r'
    elif(var == "left"):
        var = 'l'
    else:
        var = input("Enter right(r) or left(l) eye: ")

# #Once eye is selected, draw a green box with green text around the selected eye
# if(var == 'l'):
#     eye = patient[1]
#     cv2.rectangle(boxed_img, pt1, pt2, color=(0, 255, 0), thickness=2)
#     cv2.putText(boxed_img, 'Left', (pt1[0], pt1[1] + 100), font, 1, (0, 255, 0), 2, cv2.LINE_4) 
    
# else:
#     pt1 = (int(eyes[0][0] - 35), int(eyes[0][1] - 35))
#     pt2 = (int(eyes[0][0] + 35) , int(eyes[0][1] + 35))
#     cv2.rectangle(boxed_img, pt1, pt2, color=(0, 255, 0), thickness=2)
#     cv2.putText(boxed_img, 'Right', (pt1[0], pt1[1] + 100), font, 1, (0, 255, 0), 2, cv2.LINE_4) 

#display patient with boxes around eyes
i = 0
while i < 30:
    ret, img = cap.read()
    boxed_img = img
    #Once eye is selected, draw a green box with green text around the selected eye
    if(var == 'l'):
        eye = patient[1]
        cv2.rectangle(boxed_img, pt1, pt2, color=(0, 255, 0), thickness=2)
        cv2.putText(boxed_img, 'Left', (pt1[0], pt1[1] + 100), font, 1, (0, 255, 0), 2, cv2.LINE_4) 
        
    else:
        pt1 = (int(eyes[0][0] - 35), int(eyes[0][1] - 35))
        pt2 = (int(eyes[0][0] + 35) , int(eyes[0][1] + 35))
        cv2.rectangle(boxed_img, pt1, pt2, color=(0, 255, 0), thickness=2)
        cv2.putText(boxed_img, 'Right', (pt1[0], pt1[1] + 100), font, 1, (0, 255, 0), 2, cv2.LINE_4) 

    cv2.imshow('Patient Eyes', boxed_img)
    cv2.waitKey(30)
    i += 1

cv2.destroyAllWindows()
cap.release()
cap = cv2.VideoCapture(0) 

size = 100
y = int(eye[1])
x = int(eye[0])
y1 = y - size
y2 = y + size
x1 = x - size
x2 = x + size

try:
    while 1:
        ret, img = cap.read()
        resized_cropped = np.asarray([])
        cropped = img[y1:y2, x1:x2]

        if(size > 30):
            print(x, y)
            y1 = y - size
            y2 = y + size
            x1 = x - size
            x2 = x + size
            size -= 1
            # if(size > 40):

        elif(size == 30):
            #img = cropped
            gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.blur(gray, (3, 3)) 
            detected_circles = cv2.HoughCircles(gray_blurred,  
                            cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                        param2 = 30, minRadius = 1, maxRadius = 40)
            
            #find the iris and recenter image based on iris
            if detected_circles is not None: 
                detected_circles = np.uint16(np.around(detected_circles)) 
            
                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2] 
                    print(a, b, r)
                    # Draw the circumference of the circle. 
                    #size = 2*r
                    cv2.circle(cropped, (a, b), r, (0, 255, 0), 2)
                    # Draw a small circle (of radius 1) to show the center. 
                    cv2.circle(cropped, (a, b), 1, (0, 0, 255), 3) 
                    size -=1

                h, w, c = cropped.shape
                d = 2*r #diameter
                print(a, b)
                print(h,w)
                #cv2.imwrite('before.png',img[y1:y2, x1:x2])

                move_y = b - int(w/2)
                move_x = a - int(h/2)
                y1 += move_y
                y2 += move_y
                x1 += move_x
                x2 += move_x
                print(y1,y2,x1,x2)
                #cv2.imwrite('after.png',img[y1:y2, x1:x2])

        else:
            if(size > d):
                y1 += 1
                y2 -= 1
                x1 += 1
                x2 -= 1
                size -= 1

        try:
            resized_cropped = cv2.resize(cropped, (width, height))
            #print("RESIZED:", resized_cropped.shape)
        except:
            pass

        if not all(resized_cropped.shape):
            resized_cropped = img

        cv2.imshow('Surgical Camera View',resized_cropped)

        k = cv2.waitKey(30) & 0xff
        
    #cv2.imwrite('final_image.png',resized_cropped)
    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()

except OSError:
    print(OSError)