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

def moveRobotToPatient(robot=0, left=False, patient=[[]], videoSource=0, sleep_time=2.5):
        # Assign coordinates of QRCode to Robot object\
        print(videoSource)
        cap = cv2.VideoCapture(videoSource)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        robot.updateCoords(cap)

        # Get coordinates of patient's correct eye
        # potentially the wrong eye
        if (left):
            eyeX = (patient[0][0] / 640) * 1920
            eyeY = (patient[0][1] / 480) * 1080
        else:
            eyeX = (patient[1][0] / 640) * 1920
            eyeY = (patient[1][1] / 480) * 1080

        # Calculate the distance between the robot and the eye
        # Instantiate the var that will update as the robot is moving that will determine if the stop command is sent.
        distanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)
        newDistanceToEye = calc2DDistance(robot.getX(),robot.getY(),eyeX,eyeY)

        # Repeat this block for each direction, to make sure each direction gets atleast one chance to move the robot closer.
        # Robot moves in one direction, then consistently updates its coordinates and its distance to the eye.
        # If the new distance to the eye is greater than the previous difference, the loop breaks and the robot stops
        # If the distance to the eye is less than 15 pixels, the function returns
        # Once the robot stops, the newDistance is set to the baseline distance, and the robot begins again in a new direction until it returns.
        
        final_distance_to_eye = 15

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
                cap.release()
                cv2.destroyAllWindows()
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
                cap.release()
                cv2.destroyAllWindows()
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
                cap.release()
                cv2.destroyAllWindows()
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
                cap.release()
                cv2.destroyAllWindows()
                return True
        distanceToEye = newDistanceToEye

        cap.release()
        cv2.destroyAllWindows()
        return moveRobotToPatient(robot, left, patient, videoSource, sleep_time)

def getPatient(source):
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    cap = cv2.VideoCapture(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ret, frame = cap.read()

    maxImageHeight = frame.shape[0]
    maxImageWidth = frame.shape[1]

    cap.release()
    cv2.destroyAllWindows()

    patient = fd.start(fd.videoSources[source], False)
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
        #self.__controller.sendRobotCommand(self.__controller.commands["initial"])

    def updateCoords(self, cap):
        t = time.process_time()
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
        centerX = (topRight.x + bottomRight.x) / 2
        centerY = (topRight.y + bottomRight.y) / 2
        self.setX(centerX)
        self.setY(centerY)

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

    # def trackEye(self, videoSource):
    #     cap = cv2.VideoCapture(videoSource)
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    #     lk_params = dict( winSize  = (15,15),
    #               maxLevel = 2,
    #               criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    #     color = np.random.randint(0,255,(150,3))

    #     ret, frame = cap.read()
    #     prevFrame = frame
    #     old_gray = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)

    #     p0 = cv2.goodFeaturesToTrack(old_gray, 150, 0.1, 2)

    #     mask = np.zeros_like(prevFrame)
    #     xAvg = 0
    #     yAvg = 0

    #     while (1):
    #         ret, frame = cap.read()
    #         currFrame = frame
    #         frame_gray = cv2.cvtColor(currFrame, cv2.COLOR_BGR2GRAY)
    #         print("init init",frame_gray.shape)
    #         if yAvg < 0:
    #             frame_gray = frame_gray[:len(frame_gray)+round(yAvg)]
    #         elif yAvg > 0:
    #             frame_gray = frame_gray[round(yAvg):]
    #         print("init 2", frame_gray.shape)
    #         print("init old", old_gray.shape)
    #         p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None,**lk_params)

    #         goodOld = p0[st==1]
    #         goodNew = p1[st==1]
    #         goodDiff = goodNew - goodOld
    #         # print(goodDiff)
    #         # print(len(goodDiff))
    #         col_totals = [ sum(x) for x in zip(*goodDiff) ]
    #         xSum = col_totals[0]
    #         ySum = col_totals[1]
    #         xAvg = xSum / len(goodDiff)
    #         yAvg = ySum / len(goodDiff)
    #         print("xAvg: ", xAvg)
    #         print("yAvg: ", yAvg)

    #         for i,(new,old) in enumerate(zip(goodNew,goodOld)):
    #             a,b = new.ravel()
    #             c,d = old.ravel()
    #             mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
    #             frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    #         img = cv2.add(frame,mask)
    #         # print(img)
    #         if yAvg < 0:
    #             img = img[:len(img)+round(yAvg)]
    #             frame_gray = frame_gray[:len(frame_gray)+round(yAvg)]
    #         elif yAvg > 0:
    #             img = img[round(yAvg):]
    #             frame_gray = frame_gray[round(yAvg):]
    #         print("postCheck", frame_gray.shape)
    #         cv2.imshow('frame',img)
    #         k = cv2.waitKey(30) & 0xff
    #         if k == 27:
    #             break

    #         old_gray = frame_gray.copy()
    #         p0 = goodNew.reshape(-1,1,2)
    #     cap.release()

if __name__ == "__main__":
    robot = Robot()
    robot.initial()
    print("Robot Initialized")
    time.sleep(3)
    patient = getPatient("overhead")
    print("Patient Identified")
    moveRobotToPatient(robot=robot, left=False, patient=patient, videoSource=1)