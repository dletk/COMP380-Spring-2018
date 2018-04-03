from ev3dev.ev3 import *

# Connect Pixy cam and set numNodes
pixy = Sensor(address=INPUT_4)
assert pixy.connected, "Error while connecting the cam"
pixy.mode = "SIG1"

while True:
    if pixy.value(0) > 0:
        print("====> Value read: ", pixy.value())
        x = pixy.value(1)
        y = pixy.value(2)
        print(x, y)
