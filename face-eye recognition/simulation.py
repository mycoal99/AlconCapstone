import numpy as np
import cv2
import math
from demo_facenet_webcam import FaceDetector
from demo_facenet_webcam import MTCNN
import sys
import string
from stream import Streamer
import imageio
import os
from PIL import Image
import time

if __name__ == "__main__":

	stream = Streamer()
	stream.default()

	mtcnn = MTCNN(post_process=False, device='cuda')
	#Runs facial detection False runs for x frames, while true waits for true	
	x_pixelsToMove = 201
	y_pixelsToMove = 201
	firstRun = 0;
	while((abs(x_pixelsToMove) > 200) or (abs(y_pixelsToMove) > 200)):

		fd = FaceDetector(mtcnn)
		patient = fd.start(fd.videoSources["iv"],False,2)
		eyes = [patient[0], patient[1]] 			


		x_location = (eyes[0][0] + eyes[1][0])/2
		x_pixelsToMove = x_location - (2560/2)
		print("x_location: " + str(x_location))
		print("x_pixelsToMove: " + str(x_pixelsToMove))

		y_location = (eyes[0][1] + eyes[1][1])/2
		y_pixelsToMove = y_location - (1920/2)

		print("y_location: " + str(y_location))
		print("y_pixelsToMove: " + str(y_pixelsToMove))

		if(x_pixelsToMove < -200):
			stream.setLeft(abs(x_pixelsToMove/4000))
		elif(x_pixelsToMove > 200):
			stream.setRight(abs(x_pixelsToMove/4000))

		if(y_pixelsToMove > 200):
			stream.setDown(0.001)
		elif(y_pixelsToMove < -200):
			stream.setUp(0.001)
		eyes = [patient[0], patient[1]]

	stream.setZoom()



