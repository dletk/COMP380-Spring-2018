from SturdyRobot import *


def followWall():
    """Making the robot to follow a wall of the maze."""
    # robot.pointerTo(90)
    distance_to_wall = robot.readDistance()
    while robot.readTouch()[0] != 1:
        robot.forward(0.2, 0.5)
        print("====> Distance: ", distance_to_wall)
        if distance_to_wall < 15:
            robot.stop()
            robot.turnLeft(0.3, 0.1)
            robot.forward(0.3, 0.2)
            # too much to right
            robot_heading = robot.readHeading()
            if robot_heading <= 90 and robot_heading > 10:
                while robot_heading <= 10:
                    print("Heading too right: ", robot_heading)
                    robot.turnLeft(0.1, 0.2)
                    robot_heading = robot.readHeading()
            # too much to left
            elif robot_heading >= 270 and robot_heading < 350:
                while robot_heading <= 350:
                    print("Heading too left: ", robot_heading)

                    robot.turnRight(0.1, 0.2)
                    robot_heading = robot.readHeading()
        distance_to_wall = robot.readDistance()
    # Check whether there is a turn or just a go too far
    # if distance_to_wall > 25:
        # There is a turn
    robot.backward(0.2,0.3)
    robot.turnExact90()
    robot.forward(0.5, 1)


robot = SturdyRobot('A')
followWall()
