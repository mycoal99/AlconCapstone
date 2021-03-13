from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty, BooleanProperty,
                             ReferenceListProperty, StringProperty)
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from robot_controller import Robot, moveRobotToPatient, getPatient, moveRobot
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.core.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
# from kivymd.toast.kivytoast.kivytoast import Toast
from kivymd.toast.kivytoast.kivytoast import toast
from patient_db import get_patient_by_eye_template, get_patient_by_lastname
from iris_detection import moveRobotToEye
from cv2 import cv2
import _thread
from verify import verify
import time
import concurrent.futures
import threading
import multiprocessing
import asyncio


def verifying(cap):
    patientData = None
    if patientData is None:
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imwrite("eyelastmoment.png", frame)
        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, 0)
        patientData = verify(frame)
    cap.release()
    return patientData


class Gui(Widget):
    camIsShown = BooleanProperty(True)
    camera = ObjectProperty(None)
    start_button = ObjectProperty(None)
    focus_button = ObjectProperty(None)
    reset_button = ObjectProperty(None)
    name_label = StringProperty()
    dob_label = StringProperty()
    surgery_label = StringProperty()
    eye_label = StringProperty()
    robot = None
    overHeadCam = None

    def start(self, button):
        # Lines up camera with patient.
        self.robot = Robot()
        # t = threading.Thread(target=self.robot.initial, args=())
        # t.start()

        if self.ids['leftEyeToggle'].state == "down":   
            t = threading.Thread(target=moveRobot,args=(self.robot, True, [[]], 1))
            t.start()
        elif self.ids['rightEyeToggle'].state == "down":
            t = threading.Thread(target=moveRobot,args=(self.robot, False, [[]], 1))
            t.start()
        else:
            toast(text="Please select eye")
            print("Please select eye")

            
    #NEEDS TO BE CHANGED
    def focus(self, button):
        # Focuses surgical camera on patient's eFye.
        camera = self.ids['surgery_video']
        camera.capture.release()
        self.robot = Robot()
        # t.join()
        t1 = threading.Thread(target=moveRobotToEye, args=(self.robot, 0))
        t1.start()

        #maybe call join
        patientData = []
        if self.ids['leftEyeToggle'].state == "down":   
            patientData = get_patient_by_eye_template("left", verify(templateImage))
        elif self.ids['rightEyeToggle'].state == "down":
            patientData = get_patient_by_eye_template("right",  verify(templateImage))
        else:
            toast("Please select Eye")
            # print("Please select eye")
            cv2.waitKey(10)
        t1.join()

        self.camIsShown = True
        camera.capture.release()
        camera.capture = cv2.VideoCapture(0)

        if not patientData:
            raise Exception("Patient not found.")

        t2 = threading.Thread(target=self.populatePatientData, args=(patientData[0],))
        t2.start()
        # _thread.start_new_thread(self.populatePatientData, (patientData[0],))

        camera.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        Clock.schedule_interval(camera.update, 1.0/23)


    def reset(self, button):
        # Resets Robot back to initial position  
        camera = self.ids['surgery_video']
        camera.capture.release()
        self.robot = Robot()
        self.robot.initial()
        camera.capture = cv2.VideoCapture(0)
        self.camIsShown = True
        
    def populatePatientData(self, patientData):
        
        self.name_label = "Name:  {} {}".format(patientData["firstname"], patientData["lastname"])
        self.dob_label = "Date of Birth: {}".format(patientData["DOB"])
        self.surgery_label = "Surgery Type:  {}".format(patientData["surgery"])
        self.eye_label = "Surgery Eye:  {}".format(patientData["target_eye"])
        # self.eye_label = "Surgery Eye:  {}".format("whichEye")


class GuiApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.accent_hue = "A200"
        self.theme_cls.theme_style = "Dark"
        gui = Gui()
        # whichEye = Robot.getWhichEye()
        # eyeImage = Robot.getEyeImage()
        # patientInfo = getPatientInfo("whichEye", eyeImage)
        gui.name_label = "Name:  {} {}".format("---", "---") # .format(patientInfo["firstname"], patientInfo["lastname"])
        gui.dob_label = "Date of Birth: {}".format("--/--/----") # .format(patientInfo["DOB"])
        gui.surgery_label = "Surgery Type:  {}".format("---") # .format(patientInfo["surgery"])
        gui.eye_label = "Surgery Eye:  {}".format("---") # .format("whichEye")
        return gui


class MyToggleButton(MDToggleButton, MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_down = self.theme_cls.primary_dark

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.clock = Clock.schedule_interval(self.update, 1.0 / 20)
        print("KivyCam set")
    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

    # def update2(self, dt):
    #     ret, frame = self.capture.read()
    #     height, width, channels = frame.shape
    #     print(frame.shape)

    #     # zoom = 1/10
    #     # y = int(height * zoom)
    #     # y1 = int(height * (1 - zoom))
    #     # x = int(width * zoom)
    #     # x1 = int(width * (1 - zoom))

    #     # img = frame[y: y1, x: x1]
    #     # img = cv2.resize(img, (width, height))
    #     blurFrame = cv2.GaussianBlur(img, (21,21), 5)
    #     frame = cv2.addWeighted(img, 1.5, blurFrame, -0.5, 0)

    #     if ret:
    #         # convert it to texture
    #         buf1 = cv2.flip(frame, 0)
    #         buf = buf1.tostring()
    #         image_texture = Texture.create(
    #             size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    #         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    #         # display image from the texture
    #         self.texture = image_texture

if __name__ == "__main__":
    multiprocessing.freeze_support()
    GuiApp().run()