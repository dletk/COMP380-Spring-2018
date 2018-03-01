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
TIME_MOVE = 2


def followWall():
    corner = False
    foundColor = False
    while not foundColor:
        robot.forward(SPEED_MOVEMENT)
        while robot.readTouch() != (1, 1):
            pass
        robot.stop()
        if robot.readColor() == 6:
            return True
        robot.backward(SPEED_MOVEMENT, TIME_MOVE)
        if corner:
            robot.turnExact90()
            robot.turnExact90()
            # Here, we already moved to the direction of new wall, so reset corner
            corner = False
        else:
            robot.turnExact90()
        robot.forward(SPEED_MOVEMENT, 2 * TIME_MOVE)
        if robot.readTouch() == (1, 1):
            if robot.readColor() == 6:
                return True
            corner = True
        robot.backward(SPEED_MOVEMENT, TIME_MOVE)
        robot.turnExact90(side="left")


config = {SturdyRobot.RIGHT_TOUCH: "in3", SturdyRobot.LEFT_TOUCH: "in2",
          SturdyRobot.COLOR_SENSOR: "in4", SturdyRobot.GYRO_SENSOR: "in1"}

robot = SturdyRobot('A', configDict=config)
while True:
    followWall()
