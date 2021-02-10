import numpy as np
import cv2
import math
import string
import sys
import time
from scipy import signal
from robot_controller import Robot
# from scipy.ndimage import maximum_filter, minimum_filter

'''
    Assumptions:
        - one specified eye is in frame
        - no zooming or cropping of the image
        - only moving the robot arm
'''

def center(robot=0, videoSource=0, sleep_time = .5):
    EYE_CENTERED = False
    #thesholds for when the eye is centered enough
    WIDTH_THRESHOLD = 15
    HEIGHT_THESHOLD = 10

    #begin live stream
    #set surgical camera as videoSource
    cap = cv2.VideoCapture(videoSource) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    ret, img = cap.read()
    height, width, channels = img.shape
    photoNum = 0

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

            #path to save images at
            path = "C:\\Users\\Alcon\\Desktop\\eyeimages\\"
            photoName = path + "Center_Eye_" + str(sleep_time) + "_" + str(photoNum) + ".png"
            print(photoName)

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
                    cv2.circle(img, (a + int(w/2), b + int(h/2)), int((h)/3), (255, 0, 255), 2)
                    average_x[index] = a + int(w/2)
                    average_y[index] = b + int(h/2)
                    index += 1
                
                if(sum(average_x) != 0 and sum(average_y) != 0):
                    sum_x = sum(average_x)/index
                    sum_y = sum(average_y)/index
                    # print("sum_x: ", sum_x)
                    # print("sum_y: ", sum_y)
                    if(sum_x > int(width/2) - WIDTH_THRESHOLD and sum_x < int(width/2) + WIDTH_THRESHOLD 
                        and sum_y < int(height/2) + HEIGHT_THESHOLD 
                        and sum_y > int(height/2) - HEIGHT_THESHOLD):
                        EYE_CENTERED = True

                    if(sum_x < int(width/2) - WIDTH_THRESHOLD):
                        print("move right")
                        robot.right()
                        time.sleep(sleep_time)
                        robot.stop()

                    if(sum_x > int(width/2) + WIDTH_THRESHOLD):
                        print("move left")
                        robot.left()
                        time.sleep(sleep_time)
                        robot.stop()
                        
                    if(sum_y > int(height/2) + HEIGHT_THESHOLD):
                        print("move forward")
                        robot.forward()
                        time.sleep(sleep_time)
                        robot.stop()

                    if(sum_y < int(height/2) - HEIGHT_THESHOLD):
                        print("move backward")    
                        robot.backward()
                        time.sleep(sleep_time)
                        robot.stop()
                        
            #save image
            cv2.imwrite(photoName, img)
            photoNum += 1
            cv2.imshow("camera", img)
            cv2.waitKey(15)

        cap.release()
        cv2.destroyAllWindows()


    except OSError:
        print("EXCEPTION")
        print("error Center Function", OSError)


def zoom(robot=0, videoSource=0, sleep_time = .2):
    SET_UP_COMPLETE = False

    #size of iris at 200mm away
    FINAL_IRIS_SIZE = 36 #TODO

    #begin live stream
    #set surgical camera as videoSource
    cap = cv2.VideoCapture(videoSource) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
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
            #play around with param1 and param2 based on logetic zoom in
            detected_circles = cv2.HoughCircles(gray_blurred,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 40, 
                param2 = 20, minRadius = 10, maxRadius = 50)

            # find the iris and move closer to eye
            if detected_circles is not None: 
                detected_circles = np.uint16(np.around(detected_circles)) 
                print(detected_circles)
            
                for pt in detected_circles[0, :]:
                    if(pt[2] > 0):
                        a, b, r = pt[0], pt[1], pt[2] 
                        print("iris radius: ", r)
                        print("(a,b): ", "(", a, ",", b, ")")
                        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

                        #counter is used as a safety precaution
                        if(r < FINAL_IRIS_SIZE and counter < 5):
                            print("move down")
                            robot.down()
                            time.sleep(sleep_time)
                            robot.stop()
                            counter += 1

                        if (r >= FINAL_IRIS_SIZE or counter >= 5):
                            print("setup complete")
                            cv2.imwrite("Lastmoment.png", img)
                            cv2.imwrite(photoName, img)
                            SET_UP_COMPLETE = True
                            break

            #save image
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
    center(robot, videoSource, .3)
    zoom(robot, videoSource)
    center(robot, videoSource, .15)
    
    #cropping image 
    cap = cv2.VideoCapture(videoSource)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    ret, frame = cap.read()
    height, width, channels = frame.shape

    zoom = 1/3
    y = int(height * zoom)
    y1 = int(height * (1 - zoom))
    x = int(width * zoom)
    x1 = int(width * (1 - zoom))
    
    img = frame[y: y1, x: x1]
    img = cv2.resize(img, (width, height),interpolation = cv2.INTER_AREA)

    #enhance image
    blurFrame = cv2.GaussianBlur(img, (21,21), 5)
    sharpFrame = cv2.addWeighted(img, 1.5, blurFrame, -0.5, 0)
    img = sharpFrame

#     while(True):
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         height, width, channels = frame.shape
#         # (480, 640, 3)

#         zoom = 1/3
#         y = int(height * zoom)
#         y1 = int(height * (1 - zoom))
#         x = int(width * zoom)
#         x1 = int(width * (1 - zoom))
        
#         img = frame[y: y1, x: x1]
#         img = cv2.resize(img, (width, height))

#         blurFrame = cv2.GaussianBlur(img, (21,21), 5)
#         sharpFrame = cv2.addWeighted(img, 1.5, blurFrame, -0.5, 0)

#         # Our operations on the frame come here

#         # Display the resulting frame
#         #cv2.imshow('frame',img[::-1])
#         cv2.imshow('img',sharpFrame)
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # When everything done, release the capture
#     cap.release()
#     cv2.destroyAllWindows()


'''
    Assumptions:
        - two eyes is in frame
'''


if __name__ == "__main__":
    # #potentially use patient detention again and zoom in from there
    robot = Robot()
    #new initialized it is set to initial position... need to fix that
    moveRobotToEye(robot=robot, videoSource=0)
    #     # seperate center and zoom functionality
    #     # change sleep parameters
    #     # call center then zoom then center
    #     # decrease range of error for centering
