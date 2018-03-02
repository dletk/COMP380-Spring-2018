from SturdyRobot import *

SPEED_MOVEMENT = 0.05
TIME_MOVE = 2.0


def foundTouch():
    """Method to indentify which touch whether the robot touches a wall, and which touched was that."""
    touch = robot.readTouch()
    if touch == (0, 0):
        return (False, None)
    elif touch == (1, 1):
        return (True, touch)
    else:
        # Repeat the touch 2 times so we can be sure which side is touched
        for i in range(2):
            robot.backward(SPEED_MOVEMENT, TIME_MOVE / 2)
            robot.forward(SPEED_MOVEMENT, TIME_MOVE)
            touch = robot.readTouch()
            # Give priority to the case where both sides are touched -> front wall
            if touch == (1, 1):
                return (True, touch)
        return (True, touch)


def followWall():
    """Method to follow the wall of a maze until the target color WHITE was founded."""
    rightTurn = False
    foundColor = False
    while not foundColor:
        # Go forward until there is a wall found
        robot.forward(SPEED_MOVEMENT)
        touch = foundTouch()
        while not touch[0]:
            touch = foundTouch()
        touch = touch[1]
        print("Touch 1: ", touch)

        # Check color of the current wall
        robot.stop()
        if robot.readColor() == 6:
            return True

        # Move backward and turn to process to new area
        robot.backward(SPEED_MOVEMENT, TIME_MOVE)
        robot.turnExact90()

        # If there is a right turn at this position detected earlier, make a right turn
        if rightTurn:
            robot.turnExact90()
            # Here, we already moved to the direction of new wall, so reset rightTurn
            rightTurn = False
        elif touch == (1, 0):
            # There is a left turn at this position
            robot.forward(SPEED_MOVEMENT, time=4 * TIME_MOVE)
            robot.turnExact90(side="left")
            robot.forward(SPEED_MOVEMENT, time=2 * TIME_MOVE)

        # Move forward and detect a right turn
        robot.forward(SPEED_MOVEMENT, 2 * TIME_MOVE)
        touch = foundTouch()[1]
        print("Touch 2: ", touch)

        # There is a right turn
        if touch == (1, 1):
            if robot.readColor() == 6:
                return True
            rightTurn = True

        # Move backward by half the distance moved earlier, and turn 90 degree
        # to check that wall
        robot.backward(SPEED_MOVEMENT, TIME_MOVE)
        robot.turnExact90(side="left")


config = {SturdyRobot.RIGHT_TOUCH: "in3", SturdyRobot.LEFT_TOUCH: "in2",
          SturdyRobot.COLOR_SENSOR: "in4", SturdyRobot.GYRO_SENSOR: "in1"}

starSong = [('C4', 'q'), ('C4', 'q'), ('G4', 'q'), ('G4', 'q'),
            ('A4', 'q'), ('A4', 'q'), ('G4', 'h'),
            ('F4', 'q'), ('F4', 'q'), ('E4', 'q'), ('E4', 'q'),
            ('D4', 'q'), ('D4', 'q'), ('C4', 'h')]

robot = SturdyRobot('A', configDict=config)
while True:
    if followWall():
        ev3.Sound.play_song(starSong).wait()
        break
