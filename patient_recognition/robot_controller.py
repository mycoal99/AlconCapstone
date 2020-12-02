from facenet_webcam import FaceDetector
from facenet_webcam import MTCNN
import sys
import zbar
from pyzbar import pyzbar
import math
import cv2
import time


# POTENTIAL BUG: ROBOT IS IN SAME ORIENTATION AS PATIENT, AND THEY ARE BOTH 180 DEGREES OFF FROM THE ORIENTATION OF THE OVERHEAD CAMERA.

def orientRobotSetup(robot, videoSource):
    robotOriented = False
    cap = cv2.VideoCapture(videoSource)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qrCode = pyzbar.decode(gray)
    cap.release()
    print(qrCode)
    (topLeft,topRight,bottomRight,bottomLeft) = qrCode[0].polygon

    rise = topRight.y - topLeft.y
    run = topRight.x - topLeft.x
    theta = math.atan2(rise, run)

    print(theta * (int(qrCode[0].orientation) * (math.pi / 2)))
    
    time.sleep(1)

    centerX = (topLeft.x + bottomRight.x) / 2
    centerY = (topLeft.y + bottomRight.y) / 2
    robot.setX(centerX)
    robot.setY(centerY)

    if run != 0:
        slope = rise / run
        theta = math.atan(slope) * (int(qrCode[0].orientation) * (math.pi / 2))
        robot.rotate(theta)
        rise = 0
        slope = 0
    else:
        if rise > 0:
            robot.rotate90CW()
        elif rise < 0:
            robot.rotate90CCW()


    if slope == 0:
        if run > 0:
            robotOriented = True
        elif run < 0:
            robot.rotate180()
            robotOriented = True

    return robotOriented

def orientRobotFinish(robot = 0, patientInfo = 0):
    patientOrientation = patientInfo[5]
    robot.rotate(patientOrientation)

def moveCloser(robot = 0, left = False, patientInfo = 0):
    if (left):
        goalx = patientInfo[0][0]
        goaly = patientInfo[0][1]
    else:
        goalx = patientInfo[1][0]
        goaly = patientInfo[1][1]
    robotx = robot.getX()
    roboty = robot.getY()
    while ( (robotx != goalx) and (roboty != goaly) ):
        if robotx < goalx:
            robot.right()
        elif robotx > goalx:
            robot.left()
        if roboty < goaly:
            robot.up()
        elif roboty > goaly:
            robot.down()

    return True

class Robot(object):

    __xCoordinate = 0
    __yCoordinate = 0

    def __init__(self):
        __xCoordinate = 0
        __yCoordinate = 0

    # def __init__(x,y):
    #     self.__xCoordinate = x
    #     self.__yCoordinate = y

    def setX(self, x):
        self.__xCoordinate = x

    def setY(self, y):
        self.__yCoordinate = y

    def getX(self):
        return self.__xCoordinate

    def getY(self):
        return self.__yCoordinate

    def right(self):
        print("MOVE ROBOT RIGHT")
    def left(self):
        print("MOVE ROBOT LEFT")
    def up(self):
        print("MOVE ROBOT UP")
    def down(self):
        print("MOVE ROBOT DOWN")
    
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
    orientRobotSetup(robot, fd.videoSources[sys.argv[1]])
    print(robot.getX())
    print(robot.getY())
    print(patient)