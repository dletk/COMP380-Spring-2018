from SturdyRobot import *



def followWall():
    #robot.pointerTo(90)
    while robot.readDistance()<20:
        robot.forward(0.2,0.5)
        if robot.readDistance()<15:
            robot.stop()
            robot.turnLeft(0.3,0.1)
            robot.forward(0.3,0.2)
            #too much to right
            robo_heading = robot.readHeading()
            if robo_heading<=90 and robo_heading>10:
                while robo_heading<= 10:
                    print("Heading too right: ",robo_heading)
                    robot.turnLeft(0.1,0.2)
                    robo_heading = robot.readHeading()
            #
            elif robo_heading >=270 and robo_heading<350:
                while robo_heading>=350:
                    print("Heading too left: ",robo_heading)

                    robot.turnRight(0.1,0.2)
                    robo_heading = robot.readHeading()


robot = SturdyRobot('A')
followWall()
