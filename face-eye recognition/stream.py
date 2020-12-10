import cv2
import requests
import json
import time
import keyboard
import tkinter

class Streamer:

# STREAM_LINK = 'rtsp://admin:sharkboyseth@192.168.0.23:554//h264Preview_01_main'
# cap = cv2.VideoCapture(STREAM_LINK)
# cap.open(STREAM_LINK)

# ret, frame = cap.read()

# Static IP address for Michael's Reolink camera
	def __init__(self):
		self.URL = '"http://192.168.0.23"'
		self.host = '"192.168.0.23"'

		self.cred = "[" + '{"cmd" : "Login","action" : 0,"param" : {"User":{"userName":"admin","password":"sharkboyseth"}' + "}" + "}]"

		self.left = "[" + '{"cmd":"PtzCtrl","action":0,"param":{"channel":0,"op":"left","speed":1}' + '}]'
		self.right = "[" + '{"cmd":"PtzCtrl","action":0,"param":{"channel":0,"op":"right","speed":1}' + '}]'
		self.up = "[" + '{"cmd":"PtzCtrl","action":0,"param":{"channel":0,"op":"up","speed":1}' + '}]'
		self.down = "[" + '{"cmd":"PtzCtrl","action":0,"param":{"channel":0,"op":"down","speed":1}' + '}]'
		self.stop = "[" + '{"cmd":"PtzCtrl","action":0,"param":{"channel":0,"op":"Stop"}' + '}]'
		self.getZoomFocus = "[" + '{"cmd":"GetZoomFocus","action":0,"param":{"channel":0,"op":"Stop"}' + '}]'
		self.zoom = "[" + '{"cmd":"StartZoomFocus","action":0,"param":{"ZoomFocus":{"channel":0,"pos":32,"op":"ZoomPos"}' + '}' + '}]'
		self.defaultZoom = "[" + '{"cmd":"StartZoomFocus","action":0,"param":{"ZoomFocus":{"channel":0,"pos":0,"op":"ZoomPos"}' + '}' + '}]'
		self.head = {
			"Host": self.host,
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate",
			"Content-Type": "application/json",
			"X-Requested-With": "XMLHttpRequest",
			"Content-Length": "76",
			"Origin": self.URL,
			"Connection": "keep-alive",
			"Referer": self.URL
		}
		with requests.Session() as self.s:
			self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=f3d221d744421dd', data = self.cred, headers = self.head)
			self.json = self.p.json()
			self.Token = self.json[0]['value']['Token']['name']

	def userSession(self):
		with requests.Session() as s:
			# p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=f3d221d744421dd', data = self.cred, headers = self.head)
			# json = p.json()
			# Token = json[0]['value']['Token']['name']
			Token = "074715f803966f6"
			while True:
				if keyboard.is_pressed('r'):  # if key 'q' is pressed 
					p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + Token, data = self.right, headers = self.head)
					time.sleep(2)
					p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + Token, data = self.stop, headers = self.head)
					p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + Token, data = self.getZoomFocus, headers = self.head)
				elif keyboard.is_pressed('l'):
					p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + Token, data = self.left, headers = self.head)
					time.sleep(2)
					p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + Token, data = self.stop, headers = self.head)
					p = s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + Token, data = self.getZoomFocus, headers = self.head)
				elif keyboard.is_pressed('q'):
					break

	def setRight(self,timeToSleep):
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.right, headers = self.head)
		time.sleep(timeToSleep)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.stop, headers = self.head)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.getZoomFocus, headers = self.head)					

	def setLeft(self,timeToSleep):
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.left, headers = self.head)
		time.sleep(timeToSleep)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.stop, headers = self.head)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.getZoomFocus, headers = self.head)	

	def setUp(self,timeToSleep):
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.up, headers = self.head)
		time.sleep(timeToSleep)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.stop, headers = self.head)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.getZoomFocus, headers = self.head)					

	def setDown(self,timeToSleep):
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.down, headers = self.head)
		time.sleep(timeToSleep)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.stop, headers = self.head)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.getZoomFocus, headers = self.head)				

	def setZoom(self):
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.zoom, headers = self.head)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.getZoomFocus, headers = self.head)	

	def default(self):
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.defaultZoom, headers = self.head)
		self.p = self.s.post('http://192.168.0.23/cgi-bin/api.cgi?cmd=Login&token=' + self.Token, data = self.getZoomFocus, headers = self.head)

# Poll indefinitely for actions
# while True:
# 	ret,frame = cap.read()
# 	cv2.imshow('Video',frame)
# 	cv2.waitKey(1)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		cap.release()
# 		break

# cv2.destroyAllWindows()