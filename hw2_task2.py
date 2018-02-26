from SturdyRobot import *
import random

robot = SturdyRobot("A")
#TODO add beep
ev3.Sound.beep()
def findLight():
    robot.setHeading()
    reflectances = []
    heading = robot.readHeading()
    print("HEADING BEFORE: ",heading)
    while heading <= 330:
        reflectances.append(robot.readAmbient())
        robot.turnRight(0.1, 0.2)
        heading = robot.readHeading()
    robot.stop()
    robot.setHeading()
    print("===> Set heading: ", robot.readHeading())
    print(reflectances)
    print(robot.readHeading())
    max_reflectance = max(reflectances)
    ambience = robot.readAmbient()
    while ambience < max_reflectance:
        # Keep the while loop running until we found the max
        print(ambience)
        ambience = robot.readAmbient()
        robot.turnRight(0.1, 0.2)
        pass
    robot.stop()
    robot.forward(0.2,0.5)

def comfortZone():
    if robot.readDistance() < 15:
        robot.backward(0.3,0.5)
    robot.pointerLeft(time=0.1)
    if robot.readDistance() < 15:
        robot.turnRight(0.2,0.2)
        robot.forward(0.2,0.5)
    robot.zeroPointer()
    robot.pointerTo(90)
    if robot.readDistance() < 15:
        robot.turnLeft(0.2,0.2)
        robot.forward(0.2,0.5)
    robot.zeroPointer()

def followWall():
    #assume robot in the middle of box
    robot.pointerRight(time=0.3)

while True:
    comfortZone()
    findLight()
