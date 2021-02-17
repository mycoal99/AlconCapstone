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
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from patient_db import get_patient_by_eye_template
from iris_detection import moveRobotToEye

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
        robot = Robot()
        if self.ids['leftEyeToggle'].state == "down":   
            moveRobotToPatient(robot, True, getPatient(), 1)
        elif self.ids['rightEyeToggle'].state == "down":
            moveRobotToPatient(robot, False, getPatient(), 1)
        else:
            print("Please select eye")
    def focus(self, button):
        # Focuses surgical camera on patient's eye.
        camera = self.ids['surgery_video']
        camera.export_to_png("eye_template.png")
        camera.play = False
        camera._camera.stop()
        if self.ids['leftEyeToggle'].state == "down":   
            get_patient_by_eye_template("left", "eye_template.png")
        elif self.ids['rightEyeToggle'].state == "down":
            get_patient_by_eye_template("right", "eye_template.png")
        else:
            print("Please select eye")
        # get_patient_by_eye_template("left", "eye_template.png")
        self.camIsShown = False
        # moveRobotToEye(robot, 0)
        self.camIsShown = True
        pass
    def reset(self, button):
        # Resets Robot back to initial position
        # robot.initial()
        camera = self.ids['surgery_video']
        camera._camera.start()
        self.camIsShown = True
        pass
    def switchEye(self, button):
        # Switches from left eye to right eye
        pass


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


class myToggleButton(MDToggleButton, MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_down = self.theme_cls.primary_dark

if __name__ == "__main__":
    GuiApp().run()