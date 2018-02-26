from SturdyRobot import *
import random

SPEED_MOVEMENT = 0.4
SPEED_TURN = 0.1


def findLight():
    # Set the current heaiding of the robot
    robot.setHeading()
    # ------ Variables to store the maximum light intensity and its angle
    max_ambience_intensity = -1
    max_ambience_turn_count = 0

    # Turn around and gather the ambient light intensity
    turn_count = 0
    robot.readAmbient()  # This call is used to set the mode of color sensor
    heading = robot.readHeading()
    print("HEADING BEFORE: ", heading)
    while heading <= 330:
        # Check to see whether there is a new max ambience intensity found
        current_ambience_intensity = robot.readAmbient()
        if current_ambience_intensity > max_ambience_intensity:
            max_ambience_intensity = current_ambience_intensity
            max_ambience_turn_count = turn_count

        # Keep turning
        robot.turnRight(SPEED_TURN, 0.2)
        turn_count += 1
        heading = robot.readHeading()

    # After turn 1 circle, stop the robot, set the heading to current heading
    robot.stop()
    robot.setHeading()
    print("===> Set heading: ", robot.readHeading())

    # Turn the robot back to the location where it found the max ambience
    for i in range(turn_count):
        robot.turnRight(SPEED_TURN, 0.2)

    robot.stop()
    robot.forward(SPEED_MOVEMENT, 0.5)


def comfortZone():
    if robot.readDistance() < 15:
        robot.backward(SPEED_MOVEMENT, 0.5)
        return False

    robot.pointerLeft(time=0.1)
    if robot.readDistance() < 15:
        robot.turnRight(SPEED_MOVEMENT, 0.2)
        robot.forward(SPEED_MOVEMENT, 0.5)
        return False

    robot.zeroPointer()
    robot.pointerTo(90)
    if robot.readDistance() < 15:
        robot.turnLeft(SPEED_MOVEMENT, 0.2)
        robot.forward(SPEED_MOVEMENT, 0.5)
        return False

    robot.zeroPointer()
    return True


def followWall():
    # assume robot in the middle of box
    robot.pointerRight(time=0.3)


robot = SturdyRobot("A")
ev3.Sound.beep()

while True:
    while comfortZone():
        findLight()
