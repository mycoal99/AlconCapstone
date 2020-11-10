import cv2
import numpy as np

STREAM_LINK = 'rtsp://192.168.0.28:554/h264'

cap = cv2.VideoCapture()
cap.open(STREAM_LINK)

while True:
	ret, frame = cap.read()
	window = frame[0:500, 0:500]
	cv2.imshow('Video',window)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()