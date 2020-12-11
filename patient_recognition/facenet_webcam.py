import cv2
import torch
import numpy as np
from facenet_pytorch import MTCNN
import math

class FaceDetector(object):
    """
    Face detector class
    """
# "rtsp://admin:qdEJv96DYtbd@192.168.1.30" for Ryan's ReolinkWebCam
# videoSource = "rtsp://<username>:<password>@<staticIP>" for Michael's ReolinkWebCam
# videoSource = "rtsp://<username>:<password>@<staticIP>
    videoSources = {"native" : 0,
                    "redding" : "rtsp://admin:qdEJv96DYtbd@192.168.1.30",
                    "iv" : "rtsp://admin:sharkboyseth@192.168.0.23",
                    "sj" : "rtsp://admin:<password>@<staticIP>"}

    def __init__(self, mtcnn):
        self.mtcnn = mtcnn
        # State [LeftEye[x,y], RightEye[x,y], Probability, FramesActive, Orientation]
        self.states = [] 

    def _draw(self, frame, boxes, probs, landmarks, x, debugging):
        """
        Draw landmarks and boxes for each face detected
        """
        try:
            for box, prob, ld in zip(boxes, probs, landmarks):
                if debugging:
                    # Save Frame State'
                    longestFace = 0
                    isLongest = False
                    updated = False
                    if len(self.states) != 0:
                        for state in self.states:
                            # print("2")
                            if (state[3] > longestFace):
                                longestFace = state[3]
                            if (((math.isclose(state[0][0], ld[0][0], abs_tol=50)) and (math.isclose(state[0][1], ld[0][1], abs_tol=50)))  or ((math.isclose(state[1][0], ld[1][0], abs_tol=50)) and (math.isclose(state[1][1], ld[1][1], abs_tol=50)))) and (x == state[4]):
                                state[0] = ld[0]
                                state[1] = ld[1]
                                state[3] += 1
                                if (state[3] > longestFace):
                                    isLongest = True
                                    longestFace = state[3]
                                state[2] = ((state[2] * (state[3]-1)) + prob) / state[3]
                                rise = (state[1][1] - state[0][1])
                                run = (state[1][0] - state[0][0])
                                if run != 0:
                                    state[5] = math.degrees(math.atan( rise / run )) + (90 * state[4])
                                else:
                                    if rise > 0:
                                        state[5] = math.degrees(math.pi / 2) + (90 * state[4])
                                    else:
                                        state[5] = math.degrees((3 * math.pi) / 2) + (90 * state[4])
                                updated = True
                                # print("6")
                            else:
                                # print("7")
                                continue
                            
                    else:
                        # print("3")
                        rise = (ld[1][1] - ld[0][1])
                        run = (ld[1][0] - ld[0][0])
                        if run != 0:
                            theta = math.atan( rise / run )
                        else:
                            if rise > 0:
                                theta = math.pi / 2
                            else:
                                theta = (3 * math.pi) / 2
                        self.states.append([ld[0], ld[1], prob, 1, x, math.degrees(theta) + (90 * x)])
                        updated = True

                    if updated:
                        # print("4")
                        pass
                    else:
                        # print("5")
                        rise = (ld[1][1] - ld[0][1])
                        run = (ld[1][0] - ld[0][0])
                        if run != 0:
                            theta = math.atan( rise / run )
                        else:
                            if rise > 0:
                                theta = math.pi / 2
                            else:
                                theta = (3 * math.pi) / 2
                        self.states.append([ld[0], ld[1], prob, 1, x, math.degrees(theta) + (90 * x)])


                    # Draw rectangle on frame
                    if (isLongest == False):
                        cv2.rectangle(frame,
                                    (box[0], box[1]),
                                    (box[2], box[3]),
                                    (0, 0, 255),
                                    thickness=2)

                        # Show probability
                        cv2.putText(frame, str(
                            prob), (box[2], box[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                        # Draw landmarks
                        cv2.circle(frame, tuple(ld[0]), 5, (0, 0, 255), -1)
                        cv2.circle(frame, tuple(ld[1]), 5, (0, 0, 255), -1)
                        cv2.circle(frame, tuple(ld[2]), 5, (0, 0, 255), -1)
                        cv2.circle(frame, tuple(ld[3]), 5, (0, 0, 255), -1)
                        cv2.circle(frame, tuple(ld[4]), 5, (0, 0, 255), -1)
                    
                    if (isLongest):
                        cv2.rectangle(frame,
                                    (box[0], box[1]),
                                    (box[2], box[3]),
                                    (0, 255, 0),
                                    thickness=2)

                        # Show probability
                        cv2.putText(frame, str(
                            prob), (box[2], box[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                        # Draw landmarks
                        cv2.circle(frame, tuple(ld[0]), 5, (0, 255, 0), -1)
                        cv2.circle(frame, tuple(ld[1]), 5, (0, 255, 0), -1)
                        cv2.circle(frame, tuple(ld[2]), 5, (0, 255, 0), -1)
                        cv2.circle(frame, tuple(ld[3]), 5, (0, 255, 0), -1)
                        cv2.circle(frame, tuple(ld[4]), 5, (0, 255, 0), -1)

                

        except:
            pass

        return frame

    def run(self, videoSource, debugging, framesActive):
        """
            Run the FaceDetector and draw landmarks and boxes around detected faces
        """
        cap = cv2.VideoCapture(videoSource)
        i = 0
        while True:
            ret, frame = cap.read()
            for x in range(4): 
                if x == 0:
                    pass
                elif x == 1:
                    frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
                elif x == 2:
                    frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
                elif x == 3:
                    frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
                try:
                    # detect face box, probability and landmarks
                    boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
                    # draw on frame
                    self._draw(frame, boxes, probs, landmarks, x, debugging)
                    i += 1

                except:
                    pass

            # Show the frame
            if debugging:
                frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
                cv2.imshow('Patient Detection', frame)
            else:
                if i > framesActive:
                    break
                

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Usage: fcd.start(videoSource (default videoSources["native"] which is internal camera),
    # debugging (default to False which means no display boxes))
    # videoSource = videoSources["redding"] for Ryan's ReolinkWebCam
    # videoSource = videoSources["iv"] for Michael's ReolinkWebCam
    # videoSource = videoSources["sj"] for Brent's ReolinkWebCam
    # debugging = False (default) for no video display, runs for 100 frames, True for video and box display.
    def start(self, videoSource=videoSources["native"], debugging=False, framesActive=10):
        self.run(videoSource, debugging, framesActive)
        maxActive = self.states[0]
        for state in self.states:
            if state[3] > maxActive[3]:
                if state[2] > 0.98:
                    maxActive = state
        return maxActive

if __name__ == "__main__":
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    print(fd.start(debugging=True))