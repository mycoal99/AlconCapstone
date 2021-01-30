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

# def orientRobotSetup(robot, videoSource):
#     robotOriented = False
#     cap = cv2.VideoCapture(videoSource)
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     qrCode = pyzbar.decode(gray)
#     cap.release()
#     print(qrCode)
#     (topLeft,topRight,bottomRight,bottomLeft) = qrCode[0].polygon

#     rise = topRight.y - topLeft.y
#     run = topRight.x - topLeft.x
#     theta = math.atan2(rise, run)

#     print(theta * (int(qrCode[0].orientation) * (math.pi / 2)))
    
#     time.sleep(1)

#     centerX = (topLeft.x + bottomRight.x) / 2
#     centerY = (topLeft.y + bottomRight.y) / 2
#     robot.setX(centerX)
#     robot.setY(centerY)

#     if run != 0:
#         slope = rise / run
#         theta = math.atan(slope) * (int(qrCode[0].orientation) * (math.pi / 2))
#         robot.rotate(theta)
#         rise = 0
#         slope = 0
#     else:
#         if rise > 0:
#             robot.rotate90CW()
#         elif rise < 0:
#             robot.rotate90CCW()


#     if slope == 0:
#         if run > 0:
#             robotOriented = True
#         elif run < 0:
#             robot.rotate180()
#             robotOriented = True

#     return robotOriented

# def orientRobotFinish(robot = 0, patientInfo = 0):
#     patientOrientation = patientInfo[5]
#     robot.rotate(patientOrientation)

# def moveCloser(robot = 0, left = False, patientInfo = 0):
#     if (left):
#         goalx = patientInfo[0][0]
#         goaly = patientInfo[0][1]
#     else:
#         goalx = patientInfo[1][0]
#         goaly = patientInfo[1][1]
#     robotx = robot.getX()
#     roboty = robot.getY()
#     while ( (robotx != goalx) and (roboty != goaly) ):
#         if robotx < goalx:
#             robot.right()
#         elif robotx > goalx:
#             robot.left()
#         if roboty < goaly:
#             robot.up()
#         elif roboty > goaly:
#             robot.down()

#     return True

def calc2DDistance(x1,y1,x2,y2):
    return math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)

def moveRobotToPatient(robot=0, left=False, patient=0, videoSource=0):
    # Assign coordinates of QRCode to Robot object
    robot.updateCoords(videoSource)
    # Get coordinates of patient's correct eye
    if (left):
        eyeX = patient[1][0]
        eyeY = patient[1][1]
    else:
        eyeX = patient[0][0]
        eyeY = patient[0][1]

    # Calculate the distance between the robot and the eye
    # Instantiate the var that will update as the robot is moving that will determine if the stop command is sent.
    distanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
    newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

    # Repeat this block for each direction twice, to make sure each direction gets atleast one chance to move the robot closer.
    # Robot moves in one direction, then consistently updates its coordinates and its distance to the eye.
    # If the new distance to the eye is greater than the previous difference, the loop breaks and the robot stops
    # If the distance to the eye is less than 15 pixels, the function returns
    # Once the robot stops, the newDistance is set to the baseline distance, and the robot begins again in a new direction until it returns.
    robot.left()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.forward()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.right()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.backward()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.left()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.forward()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.right()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True
    robot.stop()
    distanceToEye = newDistanceToEye

    robot.backward()
    while newDistanceToEye <= distanceToEye:
        distanceToEye = newDistanceToEye
        robot.updateCoords(videoSource)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        if newDistanceToEye < 15:
            return True 
    robot.stop()
    distanceToEye = newDistanceToEye
    return False

def getPatient():
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    maxImageHeight = frame.shape[0]
    maxImageWidth = frame.shape[1]
    cap.release()
    patient = fd.start(1, True)
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
        self.__controller.sendRobotCommand(self.__controller.commands["initial"])

    def updateCoords(self, videoSource):
        cap = cv2.VideoCapture(videoSource)
        qrCode = []
        qrCode[0] = None
        while (qrCode[0] == None):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            qrCode = pyzbar.decode(gray)
        cap.release()

        (topLeft,topRight,bottomRight,bottomLeft) = qrCode[0].polygon
        centerX = (topLeft.x + bottomRight.x) / 2
        centerY = (topLeft.y + bottomRight.y) / 2
        robot.setX(centerX)
        robot.setY(centerY)

    def setX(self, x):
        self.__xCoordinate = x

    def setY(self, y):
        self.__yCoordinate = y

    def getX(self):
        return self.__xCoordinate

    def getY(self):
        return self.__yCoordinate

    def right(self):
        self.__controller.sendRobotCommand(self.__controller.commands["right"])
    def left(self):
        self.__controller.sendRobotCommand(self.__controller.commands["left"])
    def forward(self):
        self.__controller.sendRobotCommand(self.__controller.commands["forward"])
    def backward(self):
        self.__controller.sendRobotCommand(self.__controller.commands["backward"])
    def up(self):
        self.__controller.sendRobotCommand(self.__controller.commands["up"])
    def down(self):
        self.__controller.sendRobotCommand(self.__controller.commands["down"])
    def stop(self):
        __controller.sendRobotCommand(__controller.commands["stop"])
    def initial(self):
        __controller.sendRobotCommand(__controller.commands["initial"])


    
    def rotate(self, theta):
        print("Rotating {0} degrees".format(theta))

    def rotate180(self):
        print("Rotating 180 Degrees")

    def rotate90CW(self):
        print("Rotating 90 Degrees Clockwise")

    def rotate90CCW(self):
        print("Rotating 90 Degrees Counter-Clockwise")

if __name__ == "__main__":
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    patient = fd.start(fd.videoSources[sys.argv[1]], False)
    robot = Robot()
    print(moveRobotToPatient(robot=robot, left=False, patient=patient, videoSource=fd.videoSources[sys.argv[1]]))
    # print(robot.getX())
    # print(robot.getY())
    # print(getPatient())