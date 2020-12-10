from demo_facenet_webcam import FaceDetector
from demo_facenet_webcam import MTCNN
import sys

if __name__ == "__main__":
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    patient = fd.start(fd.videoSources["iv"],True,5)
    print(patient)