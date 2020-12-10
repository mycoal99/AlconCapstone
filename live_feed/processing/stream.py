import cv2
import numpy as np
import os
import requests

# STREAM_LINK = 'rtsp://admin:sharkboyseth@192.168.0.23:554//h264Preview_01_main'
# cap = cv2.VideoCapture(STREAM_LINK)
# cap.open(STREAM_LINK)

# ret, frame = cap.read()
# Static IP address for Michael's Reolink camera
class streamer():
	def __init__(self,URL,cred,head)
	self.URL = 'http://192.168.0.23'

	self.cred = "[" + '{"cmd" : "Login","action" : 0,"param" : {"User":{"userName":"admin","password":"sharkboyseth"}' + "}" + "}]"

	self.head = {
		"Host": "192.168.0.23",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0",
		"Accept": "*/*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Content-Type": "application/json",
		"X-Requested-With": "XMLHttpRequest",
		"Content-Length": "76",
		"Origin": "http://192.168.0.23",
		"Connection": "keep-alive",
		"Referer": "http://192.168.0.23/"
	}

	def startSession:
		with requests.Session() as s:
			p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=f3d221d744421dd',cred, headers = head)
			print(p.content)

			params= '{"cmd":"PtzCtrl","action":0,"param":{"channel":0,"op":"Right","speed":32}' + "}"
			ptzControl =  "curl 'http://192.168.0.23/cgi-bin/api.cgi?cmd=PtzCtrl&token=d9ea658668682d3' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: http://192.168.0.23' -H 'Connection: keep-alive' -H 'Referer: http://192.168.0.23/' --data-raw '"+ '[' + (params) + ']' + "'"
			os.system(ptzControl)

		# Poll indefinitely for actions
		# while True:
		# 	ret,frame = cap.read()
		# 	cv2.imshow('Video',frame)
		# 	cv2.waitKey(1)
		# 	if cv2.waitKey(1) & 0xFF == ord('q'):
		# 		cap.release()
		# 		break

		# cv2.destroyAllWindows()