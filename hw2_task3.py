from SturdyRobot import *


# New approach:
# Corner = false
# While color is not found:
# go forward until both touch sensor is 1
# Check if there is the matched color
# Backward by a distance X
# If corner then turn 180 else turn 90 to right
# Go forward by 2X
# if there is touch, check color, and remember corner = true
# Go backward by X
# Turn left

# X  = 0.5,0.5

SPEED_MOVEMENT = 0.05
TIME_MOVE = 2.0


def foundTouch():
    touch = robot.readTouch()
    if touch == (0, 0):
        return (False, None)
    elif touch == (1, 1):
        return (True, touch)
    else:
        # Repeat the touch 5 times so we can be sure which side is touched
        for i in range(2):
            robot.backward(SPEED_MOVEMENT, TIME_MOVE / 2)
            robot.forward(SPEED_MOVEMENT, TIME_MOVE / 1.6)
            touch = robot.readTouch()
            if touch == (1, 1):
                return (True, touch)
        return (True, touch)


def followWall():
    rightTurn = False
    foundColor = False
    while not foundColor:
        robot.forward(SPEED_MOVEMENT)
        touch = foundTouch()
        while not touch[0]:
            touch = foundTouch()
        touch = touch[1]
        # # TODO: Here, try to deal with turn based on touch
        print("Touch 1: ", touch)
        robot.stop()
        if robot.readColor() == 6:
            return True
        robot.backward(SPEED_MOVEMENT, TIME_MOVE)
        robot.turnExact90()
        if rightTurn:
            robot.turnExact90()
            # Here, we already moved to the direction of new wall, so reset rightTurn
            rightTurn = False
        elif touch == (1, 0):
            # There is a left turn
            robot.forward(SPEED_MOVEMENT, time=4 * TIME_MOVE)
            robot.turnExact90(side="left")
            robot.forward(SPEED_MOVEMENT, time=2 * TIME_MOVE)

        # Move forward and detect a right turn
        robot.forward(SPEED_MOVEMENT, 2 * TIME_MOVE)
        touch = foundTouch()[1]
        print("Touch 2: ", touch)
        if touch == (1, 1):
            if robot.readColor() == 6:
                return True
            rightTurn = True
        robot.backward(SPEED_MOVEMENT, TIME_MOVE)
        robot.turnExact90(side="left")


config = {SturdyRobot.RIGHT_TOUCH: "in3", SturdyRobot.LEFT_TOUCH: "in2",
          SturdyRobot.COLOR_SENSOR: "in4", SturdyRobot.GYRO_SENSOR: "in1"}

robot = SturdyRobot('A', configDict=config)
while True:
    followWall()
