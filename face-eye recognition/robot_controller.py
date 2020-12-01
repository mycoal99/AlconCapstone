from facenet_webcam import FaceDetector
from facenet_webcam import MTCNN
import sys

if __name__ == "__main__":
    mtcnn = MTCNN()
    fd = FaceDetector(mtcnn)
    patient = fd.start(fd.videoSources["redding"])
    print(patient)