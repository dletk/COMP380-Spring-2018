from SturdyRobot import *


def followWall():
    """Making the robot to follow a wall of the maze."""
    # robot.pointerTo(90)
    following_wall = True
    distance_to_wall = robot.readDistance()
    # while robot.readTouch()[0] != 1:
    # robot.forward(0.2, 0.5)
    print("====> Distance: ", distance_to_wall)
    if distance_to_wall > 20:
        # There is a right turn
        robot.forward(0.5, 0.4)
        robot.turnExact90()
        robot.forward(0.5, 0.3)
        following_wall = False
    # Too close to wall
    elif distance_to_wall > 5:
        # Too far away from the wall
        robot.stop()
        robot.turnRight(0.3, 0.1)
        robot.forward(0.3, 0.2)
        following_wall = True
    elif distance_to_wall < 15:
        robot.stop()
        robot.turnLeft(0.3, 0.1)
        robot.forward(0.3, 0.2)
        following_wall = True

    if following_wall:
        robot_heading = robot.readHeading()
        print("Current heading: ", robot_heading)
        # too much to right
        if robot_heading <= 90 and robot_heading > 3:
            while robot_heading >= 3:
                # print("Heading too right: ", robot_heading)
                robot.turnLeft(0.05, 0.1)
                robot_heading = robot.readHeading()
        # too much to left
        elif robot_heading >= 270 and robot_heading < 357:
            while robot_heading <= 357:
                # print("Heading too left: ", robot_heading)
                robot.turnRight(0.05, 0.1)
                robot_heading = robot.readHeading()
        robot.forward(0.4, 0.2)
        if robot.readColor() == 6:
            ev3.Sound.beep()
    distance_to_wall = robot.readDistance()

    # There is left turn

    # robot.backward(0.2,0.3)

    # TODO: Check if there is a white color


robot = SturdyRobot('A')
while True:
    followWall()
