from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty,
                             ReferenceListProperty)
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
    robot = None
    def start(self, button):
        if (button.text == "Start"):
            # robot = Robot()
            # moveRobotToPatient(robot, True, getPatient(), 1)
            button.text = "Stop"
            button.icon = "pause"
        elif (button.text == "Stop"):
            # robot.initial()
            button.text = "Start"
            button.icon = "play"

    # label1 = Label()
    # label1.text = "hello"
    




class GuiApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.accent_hue = "A200"
        self.theme_cls.theme_style = "Dark"
        return Gui()


if __name__ == "__main__":
    GuiApp().run()