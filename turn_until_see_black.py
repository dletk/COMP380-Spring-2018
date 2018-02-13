from SturdyRobot import *

robot = SturdyRobot("A")
cs = ev3.ColorSensor("in2")
cs.mode = 'COL-REFLECT'
#Had a hard time determing score might correspond to
#be considered black. I choose anything < 5.
while not cs.value() <5:
    # print("value is now: ",cs.value())
    # print("reflected light val is: ",cs.reflected_light_intensity)
    robot.turnRight(0.01)
robot.stop()
