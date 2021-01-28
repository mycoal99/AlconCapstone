from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty,
                             ReferenceListProperty)
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.video import Video
from kivy.uix.label import Label
from robot_controller import Robot, moveRobotToPatient, getPatient

class Gui(Widget):
    camera = ObjectProperty(None)
    start_button = ObjectProperty(None)
    robot = None
    def start(self, button):
        if (button.text == "Start"):
            robot = Robot()
            moveRobotToPatient(robot, True, getPatient(), 0)
            button.text = "Stop"
        elif (button.text == "Stop"):
            robot.initial()
            button.text = "Start"

    # label1 = Label()
    # label1.text = "hello"
    




class GuiApp(App):
    def build(self):
        gui = Gui()
        return gui


if __name__ == "__main__":
    GuiApp().run()