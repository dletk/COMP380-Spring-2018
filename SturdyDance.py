from SturdyRobot import *
import time as t

robot = SturdyRobot("A")
ev3.Sound.set_volume(100)

def playSong():
    ev3.Sound.play('robot_jazz.wav')

def dance(robot,speed,time=None):
    begin = t.time()
    playSong()
    while t.time() - begin < 30:
        robot.curve(speed,speed/2,1)#trying to go in s curve
        t.sleep(0.2)
        robot.curve(speed/2,speed,1)
        t.sleep(0.2)
        robot.forward(speed,time)# go onto the stage
        t.sleep(1.0)
        robot.turnLeft(0.5,2.5)#spin around show your stuff!
        t.sleep(0.2)
        robot.turnRight(0.5,2.5)
        t.sleep(0.2)
        robot.backward(speed,1.5*time)
        t.sleep(0.1)
        robot.pointerLeft(speed,2.5)
        t.sleep(0.1)
        robot.turnRight(0.5,3)

dance(robot,1,1)
