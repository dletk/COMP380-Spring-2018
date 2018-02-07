from SturdyRobot import *

robot = SturdyRobot("teamA")

robot.forward(0.3,5) #first
robot.wait_until_not_moving()
robot.turnRight(0.3,0.5)# about 90 deg
robot.wait_until_not_moving()
robot.forward(0.3,2.5)
robot.wait_until_not_moving()
robot.turnLeft(0.3,0.55)
robot.wait_until_not_moving()
robot.forward(0.3,2.7)
robot.wait_until_not_moving()
robot.turnLeft(0.3,0.55)
robot.wait_until_not_moving()
robot.forward(0.3, 5)
