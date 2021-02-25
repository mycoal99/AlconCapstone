from facenet_webcam import FaceDetector
from facenet_webcam import MTCNN
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from pyzbar import pyzbar
import math
import cv2
import time
from CapstoneClient import CapstoneClient

# POTENTIAL BUG: ROBOT IS IN SAME ORIENTATION AS PATIENT, AND THEY ARE BOTH 180 DEGREES OFF FROM THE ORIENTATION OF THE OVERHEAD CAMERA.

def calc2DDistance(x1,y1,x2,y2):
    return math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)

def moveRobot(robot=0, left=False, patient=[[]], videoSource=1, sleep_time=2.5):
    cap = cv2.VideoCapture(videoSource)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print("cam set")
    patient = getPatient(cap)
    moveRobotToPatient(robot, left, patient, cap)

def moveRobotToPatient(robot=0, left=False, patient=[[]], cap=0, sleep_time=2.5):
        # Assign coordinates of QRCode to Robot object\
        print("moveRobotToPatient")
        start = time.time()
        robot.updateCoords(cap)

        # Get coordinates of patient's correct eye
        # potentially the wrong eye
        
        if (left):
            eyeX = patient[0][0]
            eyeY = patient[0][1]
        else:
            eyeX = patient[1][0]
            eyeY = patient[1][1]

        # Calculate the distance between the robot and the eye
        # Instantiate the var that will update as the robot is moving that will determine if the stop command is sent.
        distanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

        final_distance_to_eye = 5

        robot.right()
        time.sleep(.7)
        robot.stop()
        distanceToEye = newDistanceToEye
        robot.updateCoords(cap)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

        while newDistanceToEye <= distanceToEye:
            print("newDistanceToEye:", newDistanceToEye, "\n")
            calc_sleep_time = newDistanceToEye/60
            print("sleep_time:", calc_sleep_time, "\n")
            robot.right()
            time.sleep(calc_sleep_time)
            robot.stop()
            distanceToEye = newDistanceToEye
            robot.updateCoords(cap)
            newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
            if newDistanceToEye < final_distance_to_eye:
                return True
        distanceToEye = newDistanceToEye

        robot.forward()
        time.sleep(.7)
        robot.stop()
        distanceToEye = newDistanceToEye
        robot.updateCoords(cap)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

        while newDistanceToEye <= distanceToEye:
            # print("forward while loop 1")
            print("newDistanceToEye:", newDistanceToEye, "\n")
            calc_sleep_time = newDistanceToEye/60
            print("sleep_time:", calc_sleep_time, "\n")
            robot.forward()
            time.sleep(calc_sleep_time)
            robot.stop()
            distanceToEye = newDistanceToEye
            robot.updateCoords(cap)
            newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

            if newDistanceToEye < final_distance_to_eye:
                return True
        distanceToEye = newDistanceToEye

        robot.left()
        time.sleep(.7)
        robot.stop()
        distanceToEye = newDistanceToEye
        robot.updateCoords(cap)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)        

        while newDistanceToEye <= distanceToEye:
            print("newDistanceToEye:", newDistanceToEye, "\n")
            calc_sleep_time = newDistanceToEye/60
            print("sleep_time:", calc_sleep_time, "\n")
            robot.left()
            time.sleep(calc_sleep_time)
            robot.stop()
            distanceToEye = newDistanceToEye
            robot.updateCoords(cap)
            newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

            if newDistanceToEye < final_distance_to_eye:
                return True
        distanceToEye = newDistanceToEye

        robot.backward()
        time.sleep(.7)
        robot.stop()
        distanceToEye = newDistanceToEye
        robot.updateCoords(cap)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

        while newDistanceToEye <= distanceToEye:
            # print("backward while loop 1")
            print("newDistanceToEye:", newDistanceToEye, "\n")
            calc_sleep_time = newDistanceToEye/60
            print("sleep_time:", calc_sleep_time, "\n")
            robot.backward()
            time.sleep(calc_sleep_time)
            robot.stop()
            distanceToEye = newDistanceToEye
            robot.updateCoords(cap)
            newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

            if newDistanceToEye < final_distance_to_eye:
                return True
        distanceToEye = newDistanceToEye

        return moveRobotToPatient(robot, left, patient, cap, sleep_time)

def getPatient(cap):
    start = time.time()
    print("get Patient")

    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)

    ret, frame = cap.read()

    maxImageHeight = frame.shape[0]
    maxImageWidth = frame.shape[1]

    patient = fd.start(cap, False)
    orientation = patient[4]
    if orientation == 0:
        pass
    elif orientation == 1:
        tempy1 = patient[0][1]
        tempy2 = patient[1][1] 
        patient[0][1] = maxImageHeight - patient[0][0]
        patient[0][0] = tempy1
        patient[1][1] = maxImageHeight - patient[1][0]
        patient[1][0] = tempy2
    elif orientation == 2:
        patient[0][0] = maxImageWidth - patient[0][0]
        patient[0][1] = maxImageHeight - patient[0][1]
        patient[1][0] = maxImageWidth - patient[1][0]
        patient[1][1] = maxImageHeight - patient[1][1]
    elif orientation == 3:
        tempx1 = patient[0][0]
        tempx2 = patient[1][0]
        patient[0][0] = maxImageWidth - patient[0][1]
        patient[0][1] = tempx1
        patient[1][0] = maxImageWidth - patient[1][1]
        patient[1][1] = tempx2
    
    print("getPatient_time: ", str(time.time() - start))
    return patient

class Robot(object):

    # __xCoordinate = 0
    # __yCoordinate = 0
    # __controller = CapstoneClient()

    def __init__(self):
        self.__xCoordinate = 0
        self.__yCoordinate = 0
        self.__controller = CapstoneClient()
        self.__controller.start()
        #self.__controller.sendRobotCommand(self.__controller.commands["initial"])

    def updateCoords(self, cap):
        start = time.time()
        print(cap)
        print("updateCoords")
        qrCode = []

        FOUND_QR = False
        while(not FOUND_QR):
            ret, frame = cap.read()
            
            blurFrame = cv2.GaussianBlur(frame, (21,21), 5)
            sharpFrame = cv2.addWeighted(frame, 1.5, blurFrame, -0.5, 0)

            x = int(self.getX())
            y = int(self.getY())

            qrCode = pyzbar.decode(sharpFrame)
            if(len(qrCode) > 0):
                if(len(qrCode[0].polygon) == 4):
                    FOUND_QR = True

        (topLeft,topRight,bottomRight,bottomLeft) = qrCode[0].polygon

        while(True):
            ret, frame = cap.read()

            # Our operations on the frame come here
            cv2.circle(frame, (int((topRight.x + bottomRight.x) / 2), int((topRight.y + bottomRight.y) / 2)), 4, (255, 255, 255), -1)
            # Display the resulting frame
            cv2.imshow('frame',frame[::-1])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        centerX = (topRight.x + bottomRight.x) / 2
        centerY = (topRight.y + bottomRight.y) / 2
        self.setX(centerX)
        self.setY(centerY)

        print("updateCoords_time:", str(time.time() - start))

    def setX(self, x):
        self.__xCoordinate = x

    def setY(self, y):
        self.__yCoordinate = y

    def getX(self):
        return self.__xCoordinate

    def getY(self):
        return self.__yCoordinate
        
    def initial(self):
        print("initial")
        self.__controller.sendRobotCommand(self.__controller.commands["initial"])
    def right(self):
        print("right")
        self.__controller.sendRobotCommand(self.__controller.commands["right"])
    def left(self):
        print("left")
        self.__controller.sendRobotCommand(self.__controller.commands["left"])
    def forward(self):
        print("forward")
        self.__controller.sendRobotCommand(self.__controller.commands["forward"])
    def backward(self):
        print("backward")
        self.__controller.sendRobotCommand(self.__controller.commands["backward"])
    def up(self):
        print("up")
        self.__controller.sendRobotCommand(self.__controller.commands["up"])
    def down(self):
        print("down")
        self.__controller.sendRobotCommand(self.__controller.commands["down"])
    def stop(self):
        print("stop")
        self.__controller.sendRobotCommand(self.__controller.commands["stop"])
    
    def rotate(self, theta):
        print("Rotating {0} degrees".format(theta))

    def rotate180(self):
        print("Rotating 180 Degrees")

    def rotate90CW(self):
        print("Rotating 90 Degrees Clockwise")

    def rotate90CCW(self):
        print("Rotating 90 Degrees Counter-Clockwise")

# if __name__ == "__main__":
#     robot = Robot()
#     robot.initial()
#     print("Robot Initialized")
#     time.sleep(3)
#     patient = getPatient("overhead")
#     print("Patient Identified")
#     moveRobotToPatient(robot=robot, left=False, patient=patient, videoSource=1)