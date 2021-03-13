import numpy as np
import cv2
import math
import string
import time
import sys
import time
from scipy import signal
from robot_controller import Robot
# from scipy.ndimage import maximum_filter, minimum_filter

'''
    Assumptions:
        - one specified eye is in frame
        - no zoomInEyeing or cropping of the image
        - only moving the robot arm
'''

def center(robot=0, cap=cv2.VideoCapture(0), sleep_time = .5):
    EYE_CENTERED = False
    print("center")
    #thesholds for when the eye is centered enough
    WIDTH_THRESHOLD = 20
    HEIGHT_THESHOLD = 15

    #begin live stream
    #set surgical camera as videoSource
    ret, img = cap.read()
    height, width, channels = img.shape

    try:
        while not EYE_CENTERED:
            ret, img = cap.read()
            height, width, channels = img.shape 

            #image processing for pupil detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (11, 11), 0)
            gray_blurred = cv2.medianBlur(gray_blurred, 3)
            threshold = cv2.threshold(gray_blurred, 15, 255, cv2.THRESH_BINARY_INV)[1]
            contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #Pupil detection
            '''
                Moving the camera to center based on the average of the center of the circles
            '''
            if type(contours[1]) != None:
                contours = sorted(contours[0], key=lambda x: cv2.contourArea(x))
                average_x = [0]*len(contours)
                average_y = [0]*len(contours)
                index = 0
                for cnt in contours:
                    (a, b, w, h) = cv2.boundingRect(cnt)
                    # cv2.circle(img, (a + int(w/2), b + int(h/2)), int((h)/3), (255, 0, 255), 2)
                    # print("x", a + int(w/2), "y", b + int(h/2))
                    if(h/3 > 0):
                        average_x[index] = a + int(w/2)
                        average_y[index] = b + int(h/2)
                        index += 1
                
                if(sum(average_x) != 0 and sum(average_y) != 0):
                    sum_x = sum(average_x)/index
                    sum_y = sum(average_y)/index
                    if(sum_x > int(width/2) - WIDTH_THRESHOLD and sum_x < int(width/2) + WIDTH_THRESHOLD 
                        and sum_y < int(height/2) + HEIGHT_THESHOLD 
                        and sum_y > int(height/2) - HEIGHT_THESHOLD):
                        EYE_CENTERED = True

                    if(sum_x < int(width/2) - WIDTH_THRESHOLD):
                        robot.right()
                        time.sleep(sleep_time)
                        robot.stop()

                    if(sum_x > int(width/2) + WIDTH_THRESHOLD):
                        robot.left()
                        time.sleep(sleep_time)
                        robot.stop()
                        
                    if(sum_y > int(height/2) + HEIGHT_THESHOLD):
                        robot.forward()
                        time.sleep(sleep_time)
                        robot.stop()

                    if(sum_y < int(height/2) - HEIGHT_THESHOLD): 
                        robot.backward()
                        time.sleep(sleep_time)
                        robot.stop()
                        
            cv2.waitKey(15)


    except OSError:
        print("EXCEPTION")
        print("error Center Function", OSError)


def zoomInEye(robot=0, cap=cv2.VideoCapture(0), sleep_time = .5):
    print("zoom")
    SET_UP_COMPLETE = False

 #size of iris at 200mm away
    FINAL_IRIS_SIZE = 200 #TODO

    #begin live stream
    #set surgical camera as videoSource
    ret, img = cap.read()
    height, width, channels = img.shape
    counter = 0
    photoNum = 0

    try:
        while not SET_UP_COMPLETE:
            ret, img = cap.read()
            height, width, channels = img.shape 

            #Iris and Pupil detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (11, 11), 0)
            gray_blurred = cv2.medianBlur(gray_blurred, 3)

            #Iris detection
            #play around with param1 and param2 based on logetic zoom in
            detected_circles = cv2.HoughCircles(gray_blurred,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 40, 
                param2 = 20, minRadius = 40, maxRadius = 200)

            # find the iris and move closer to eye
            if detected_circles is not None: 
                detected_circles = np.uint16(np.around(detected_circles)) 
                pts = detected_circles[0, :]
                pt = pts[0]
                a, b, r = pt[0], pt[1], pt[2] 
                # print("iris radius: ", r)
            
                if(r < FINAL_IRIS_SIZE and counter < 5):
                    print("move down")
                    robot.down()
                    time.sleep(sleep_time)
                    robot.stop()
                    counter += 1

                if (r >= FINAL_IRIS_SIZE or counter >= 5):
                    print("setup complete")
                    SET_UP_COMPLETE = True
                    break

            cv2.waitKey(10)

    except OSError:
        print("EXCEPTION")
        print("error line 190", OSError)


def moveRobotToEye(robot=0, videoSource=0):
    start_time = time.time()
    cap = cv2.VideoCapture(videoSource)
    print("cap_time", time.time() - start_time)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print("set_time", time.time() - start_time)
    print("cam set")

    center(robot, cap, .2)
    zoomInEye(robot, cap)
    center(robot, cap, .15)
    robot.down()
    time.sleep(.5)
    robot.stop()

    cap.release()

'''
    Assumptions:
        - two eyes is in frame
'''

# if __name__ == "__main__":
#     # #potentially use patient detention again and zoomInEye in from there
#     robot = Robot()
#     moveRobotToEye(robot=robot, videoSource=0)