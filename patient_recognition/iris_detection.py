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

def center(robot=0, videoSource=0, sleep_time = .5):
    EYE_CENTERED = False
    WIDTH_THRESHOLD = 10
    HEIGHT_THESHOLD = 5

    #begin live stream
    #set surgical camera as videoSource
    cap = cv2.VideoCapture(videoSource) 
    ret, img = cap.read()
    height, width, channels = img.shape
    counter = 0
    photoNum = 0

    # center()
    # zoom()
    # center()

    try:
        while not EYE_CENTERED:
            ret, img = cap.read()
            height, width, channels = img.shape 

            #Iris and Pupil detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (11, 11), 0)
            gray_blurred = cv2.medianBlur(gray_blurred, 3)

            threshold = cv2.threshold(gray_blurred, 15, 255, cv2.THRESH_BINARY_INV)[1]
            contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            path = "C:\\Users\\Alcon\\Desktop\\eyeimages\\"
            photoName = path + "Center_Eye_1_" + str(photoNum) + ".png"
            print(photoName)
            #Pupil detection
            if type(contours[1]) != None:
                contours = sorted(contours[0], key=lambda x: cv2.contourArea(x))
                average_a = []
                average_b = []
                index = 0 
                for cnt in contours:
                    (a, b, w, h) = cv2.boundingRect(cnt)
                    cv2.circle(img, (a + int(w/2), b + int(h/2)), int((h)/3), (255, 0, 255), 2)
                    print("counters: ", (int((h)/3)))
                    average_a[index] = a + int(w/2)
                    average_b[index] = b + int(h/2)
                    index += 1
            
                #need to find better if conditions
                # if(int(h/3) > 0 and int(h/3) < 5):
                #     print("a: ", a, ", b: ", b, ", w: ", w, ", h: ", h)
                    #set pupil in center of camera
                    #API call- move (north, south, east, west), wait, stop
                if(sum(average_a) > int(width/2) - WIDTH_THRESHOLD and sum(average_a) < int(width/2) + WIDTH_THRESHOLD
                    and sum(average_b) < int(height/2) + HEIGHT_THESHOLD and sum(average_b) > int(height/2) - HEIGHT_THESHOLD
                ):
                    EYE_CENTERED = True

                if(sum(average_a) < int(width/2) - WIDTH_THRESHOLD):
                    print("move right")
                    robot.right()
                    time.sleep(sleep_time)
                    robot.stop()

                if(sum(average_a) > int(width/2) + WIDTH_THRESHOLD):
                    print("move left")
                    robot.left()
                    time.sleep(sleep_time)
                    robot.stop()
                    
                if(sum(average_b) > int(height/2) + HEIGHT_THESHOLD):
                    print("move forward")
                    robot.forward()
                    time.sleep(sleep_time)
                    robot.stop()

                if(sum(average_b) < int(height/2) - HEIGHT_THESHOLD):
                    print("move backward")    
                    robot.backward()
                    time.sleep(sleep_time)
                    robot.stop()

            cv2.imwrite(photoName, img)
            photoNum += 1
            cv2.imshow("camera", img)
            cv2.waitKey(10)

        cap.release()
        cv2.destroyAllWindows()


    except OSError:
        print("EXCEPTION")
        print("error Center Function", OSError)


def zoom(robot=0, videoSource=0):
    SET_UP_COMPLETE = False
    FINAL_IRIS_SIZE = 35 #TODO

    #begin live stream
    #set surgical camera as videoSource
    cap = cv2.VideoCapture(videoSource) 
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

            path = "C:\\Users\\Alcon\\Desktop\\eyeimages\\"
            photoName = path + "Zoom_In_" + str(photoNum) + ".png"
            print(photoName)
            #Iris detection
            #play around with param1 and param2
            detected_circles = cv2.HoughCircles(gray_blurred,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 40, 
                param2 = 20, minRadius = 5, maxRadius = 50)

            # find the iris and move closer to eye
            if detected_circles is not None: 
                detected_circles = np.uint16(np.around(detected_circles)) 
                print(detected_circles)
            
                for pt in detected_circles[0, :]:
                    if(pt[2] > 0):
                        a, b, r = pt[0], pt[1], pt[2] 
                        #print(a, b, r)
                        print("iris radius: ", r)
                        print("(a,b): ", "(", a, ",", b, ")")
                        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                        #API call- move (up and down), wait, stop

                        if(r < FINAL_IRIS_SIZE):
                            print("move down")
                            robot.down()
                            time.sleep(.5)
                            robot.stop()
                            counter += 1

                        if (r >= FINAL_IRIS_SIZE):
                            print("setup complete")
                            cv2.imwrite("Lastmoment.png", img)
                            SET_UP_COMPLETE = True

            #move robot to closer to eye
            cv2.imwrite(photoName, img)
            photoNum += 1
            cv2.imshow("camera", img)
            cv2.waitKey(10)

        cap.release()
        cv2.destroyAllWindows()


    except OSError:
        print("EXCEPTION")
        print("error line 95", OSError)


def moveRobotToEye(robot=0, videoSource=0):
    center(robot, videoSource)
    zoom(robot, videoSource)
    center(robot, videoSource, .3)


'''
    Assumptions:
        - two eyes is in frame
'''


if __name__ == "__main__":
    #potentially use patient detention again and zoom in from there
    robot = Robot()
    #new initialized it is set to initial position... need to fix that
    moveRobotToEye(robot=robot, videoSource=0)
        # seperate center and zoom functionality
        # change sleep parameters
        # call center then zoom then center
        # decrease range of ertror for centering

