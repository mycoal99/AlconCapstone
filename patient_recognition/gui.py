from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty, BooleanProperty,
                             ReferenceListProperty, StringProperty)
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from robot_controller import Robot, moveRobotToPatient, getPatient
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.core.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
# from kivymd.toast.kivytoast.kivytoast import Toast
from kivymd.toast.kivytoast.kivytoast import toast
from patient_db import get_patient_by_eye_template
from iris_detection import moveRobotToEye
from cv2 import cv2

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
    def start(self, button):
        # Lines up camera with patient.
        self.robot = Robot()
        if self.ids['leftEyeToggle'].state == "down":   
            moveRobotToPatient(self.robot, True, getPatient("overhead"), 1)
        elif self.ids['rightEyeToggle'].state == "down":
            moveRobotToPatient(self.robot, False, getPatient("overhead"), 1)
        else:
            toast(text="Please select eye")
            print("Please select eye")
    def focus(self, button):
        # Focuses surgical camera on patient's eye.
        camera = self.ids['surgery_video']
        ret, template = camera.capture.read()
        if self.ids['leftEyeToggle'].state == "down":   
            get_patient_by_eye_template("left", template)
        elif self.ids['rightEyeToggle'].state == "down":
            get_patient_by_eye_template("right", template)
        else:
            toast("Please select Eye")
            print("Please select eye")
        self.camIsShown = False
        camera.capture.release()
        moveRobotToEye(self.robot, 0)
        camera.capture = cv2.VideoCapture(0)
        self.camIsShown = True
    def reset(self, button):
        # Resets Robot back to initial position
        self.robot.initial()
        camera = self.ids['surgery_video']
        camera.capture = cv2.VideoCapture(0)
        self.camIsShown = True


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
        Clock.schedule_interval(self.update, 1.0 / 60)

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

if __name__ == "__main__":
    GuiApp().run()