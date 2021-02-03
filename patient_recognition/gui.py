from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty,
                             ReferenceListProperty, StringProperty)
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from robot_controller import Robot, moveRobotToPatient, getPatient
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

class Gui(Widget):
    camera = ObjectProperty(None)
    start_button = ObjectProperty(None)
    focus_button = ObjectProperty(None)
    reset_button = ObjectProperty(None)
    name_label = StringProperty()
    surgery_label = StringProperty()
    eye_label = StringProperty()
    robot = None
    def start(self, button):
        # Lines up camera with patient.
        # robot = Robot()
        # moveRobotToPatient(robot, True, getPatient(), 1)
        pass
    def focus(self, button):
        # Focuses surgical camera on patient's eye.
        pass
    def reset(self, button):
        # Resets Robot back to initial position
        # robot.initial()
        pass

class GuiApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.accent_hue = "A200"
        self.theme_cls.theme_style = "Dark"
        gui = Gui()
        gui.name_label = "Name:  {}".format("Michael Who")
        gui.surgery_label = "Surgery Type:  {}".format("Cataracts")
        gui.eye_label = "Eye:  {}".format("Left")
        return gui


if __name__ == "__main__":
    GuiApp().run()