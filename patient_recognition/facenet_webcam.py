import cv2
import torch
import numpy as np
from facenet_pytorch import MTCNN
import math
import vlc

class FaceDetector(object):
    """
    Face detector class
    """

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
                    # Draw rectangle on frame
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

                # Save Frame State
                updated = False
                if len(self.states) != 0:
                    for state in self.states:
                        # print("2")
                        if (((math.isclose(state[0][0], ld[0][0], abs_tol=50)) and (math.isclose(state[0][1], ld[0][1], abs_tol=50)))  or ((math.isclose(state[1][0], ld[1][0], abs_tol=50)) and (math.isclose(state[1][1], ld[1][1], abs_tol=50)))) and (x == state[4]):
                            state[0] = ld[0]
                            state[1] = ld[1]
                            state[3] += 1
                            state[2] = ((state[2] * (state[3]-1)) + prob) / state[3]
                            updated = True
                            # print("6")
                        else:
                            # print("7")
                            continue
                else:
                    # print("3")
                    self.states.append([ld[0], ld[1], prob, 1, x])
                    updated = True

                if updated:
                    # print("4")
                    pass
                else:
                    # print("5")
                    self.states.append([ld[0], ld[1], prob, 1, x])

        except:
            pass

        return frame

    def run(self, videoSource=0, debugging=True):
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
                cv2.imshow('Face Detection', frame)
            else:
                if i > 100:
                    break
                

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
        
# Run the app
# instance = vlc.Instance()
# videoPlayer = instance.media_player_new("rtsp://192.168.1.30:554")
# videoPlayer.play()
mtcnn = MTCNN()
fcd = FaceDetector(mtcnn)
# Usage: fcd.run(videoSource (default 0 which is internal camera),
# debugging (default to True which means display boxes))
# videoSource = "rtsp://admin:qdEJv96DYtbd@192.168.1.30" for Ryan's ReolinkWebCam
# debugging = False for no video display, runs for 100 frames, True for video and box display.
fcd.run()
maxActive = fcd.states[0]
for state in fcd.states:
    if state[3] > maxActive[3]:
        if state[2] > 0.98:
            maxActive = state
print(maxActive)