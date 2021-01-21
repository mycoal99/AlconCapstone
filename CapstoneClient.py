import socket

class CapstoneClient:

  commands = {"left" : b'\x00\x00\x00\x00',
           "right" :  b'\x00\x00\x00\x01',
           "forward" :  b'\x00\x00\x00\x02',
           "backward" :  b'\x00\x00\x00\x03',
           "up" :  b'\x00\x00\x00\x04',
           "down" :  b'\x00\x00\x00\x05',
           "initial" :  b'\x00\x00\x00\x06',
           "stop" :  b'\x00\x00\x00\x07',
           "clearErrors" :  b'\x00\x00\x00\x08'}

  def __init__(self):
    self.__connected = False
  
  def start(self):
    print("Connecting to {0} port {1}".format("localhost", 7890))
    self.__connect()
    return self
  
  def sendRobotCommand(self, command):
    isConnected = self.__connected
    if isConnected:
     self.__stream.send(command)
  
  def __connect(self):
    while not self.__connected:
     self.__stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try:
       self.__stream.connect(('localhost', 7890))
     except:
       self.__connected = False
       print("Failed to connect. Retrying...")
       continue
     self.__connected = True
     print("Connected successfully. Ready to send commands.")
