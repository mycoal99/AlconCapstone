from CapstoneClient import CapstoneClient
import threading
import copy

commands = {"left" : b'\x00\x00\x00\x00',
           "right" :  b'\x00\x00\x00\x01',
           "forward" :  b'\x00\x00\x00\x02',
           "backward" :  b'\x00\x00\x00\x03',
           "up" :  b'\x00\x00\x00\x04',
           "down" :  b'\x00\x00\x00\x05',
           "initial" :  b'\x00\x00\x00\x06',
           "stop" :  b'\x00\x00\x00\x07',
           "clearErrors" :  b'\x00\x00\x00\x08'}

cc =  CapstoneClient().start()

def printHelp():
  print("\nCommands:")
  print("\tleft - Move the robot left")
  print("\tright - Move the robot right")
  print("\tforward - Move the robot backward")
  print("\tbackward - Move the robot forward")
  print("\tup - Move the robot up the z-axis")
  print("\tdown - Move the robot down the z-axis")
  print("\tinitial - Move the robot to its initial position")
  print("\tstop - Stop the robot move")
  print("\tclearErrors - Clear any robot errors")

if __name__ == '__main__':
  running = True
  while running:
    printHelp()
    command = input("\nEnter a command:\n")
    
    try:
      cc.sendRobotCommand(commands[command])
    except:
      print("Invalid command entered.")

cc.stop()