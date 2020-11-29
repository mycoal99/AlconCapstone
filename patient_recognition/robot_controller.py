from facenet_webcam import FaceDetector
from facenet_webcam import MTCNN
import sys
import zbar
import math

def orientRobotSetup(robot = 0):
    robotOriented = False
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    for result in results:
        topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in result.position]
    rise = topRightCorners[1] - topLeftCorners[1]
    run = topRightCorners[0] - topLeftCorners[0]
    if run != 0:
        slope = rise / run
        theta = math.atan(slope)
        robot.rotate(theta)
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

def moveCloser(robot = 0, left = False, patientInfo = 0, robotInfo = 0):
    if (left):
        goalx = patientInfo[0][0]
        goaly = patientInfo[0][1]
    else:
        goalx = patientInfo[1][0]
        goaly = patientInfo[1][1]
    robotx = robotInfo[0][0]
    roboty = robotInfo[0][1]
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


    

if __name__ == "__main__":
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    patient = fd.start(fd.videoSources[sys.argv[1]], True)
    print(patient)