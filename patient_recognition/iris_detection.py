import numpy as np
import cv2
import math
import string
import sys
import time
from scipy import signal
from robot_controller import Robot

# from segmentation.segmentiris import segmentiris

'''
    Assumptions:
        - one specified eye is in frame
        - no zooming or cropping of the image
        - only moving the robot arm
'''

def moveRobotToEye(robot=0, videoSource=0):

    #set surgical camera as videoSource
    VIDEO_SOURCE = videoSource
    SET_UP_COMPLETE = False
    EYELASHES_THRESHOLD = 80
    USE_MULTIPROCESSOR = False
    FINAL_IRIS_SIZE = 30 #TODO

    #begin live stream
    cap = cv2.VideoCapture(VIDEO_SOURCE) 
    ret, img = cap.read()
    height, width, channels = img.shape
    counter = 0

    try:
        while not SET_UP_COMPLETE:
            ret, img = cap.read()
            height, width, channels = img.shape 

            #Iris and Pupil detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (11, 11), 0)
            gray_blurred = cv2.medianBlur(gray_blurred, 3)

            threshold = cv2.threshold(gray_blurred, 15, 255, cv2.THRESH_BINARY_INV)[1]
            contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #Pupil detection
            if type(contours[1]) != None:
                contours = sorted(contours[0], key=lambda x: cv2.contourArea(x), reverse=True)
                for cnt in contours:
                    (a, b, w, h) = cv2.boundingRect(cnt)
                    cv2.circle(img, (a + int(w/2), b + int(h/2)), int((h)/3), (255, 0, 255), 2)
                
                    if(len(contours) == 1):
                        #set pupil in center of camera
                        #API call- move (north, south, east, west), wait, stop
                        if(a > int(w/2)):
                            print("move right")
                            robot.right()
                            time.sleep(5)
                            robot.stop()

                        if(a < int(w/2)):
                            print("move left")
                            robot.left()
                            time.sleep(5)
                            robot.stop()
                        
                        if(b > int(h/2)):
                            print("move forward")
                            robot.forward()
                            time.sleep(5)
                            robot.stop()

                        if(b < int(h/2)):
                            print("move backward")    
                            robot.backward()
                            time.sleep(5)
                            robot.stop()

            #Iris detection
            #play around with param1 and param2
            detected_circles = cv2.HoughCircles(gray_blurred,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, 
                param2 = 50, minRadius = 1, maxRadius = int(width/2))

            # find the iris and move closer to eye
            if detected_circles is not None: 
                detected_circles = np.uint16(np.around(detected_circles)) 
            
                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2] 
                    #print(a, b, r)
                    print("iris radius: ", r)
                    cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                    cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                    #API call- move (up and down), wait, stop

                    if(r < FINAL_IRIS_SIZE and counter < 5):
                        print("move down")
                        robot.down()
                        time.sleep(2)
                        robot.stop()
                        counter += 1

                    if (r >= FINAL_IRIS_SIZE or counter >= 5):
                        SET_UP_COMPLETE = true

            #move robot to closer to eye
            cv2.imshow('Surgical Camera View', img)
            k = cv2.waitKey(1) & 0xff
            
        cap.release()
        cv2.destroyAllWindows()

    except OSError:
        print("error line 95", OSError)


'''
    Assumptions:
        - two eyes is in frame
'''


if __name__ == "__main__":
    robot = Robot()
    moveRobotToEye(robot=robot, videoSource=0)