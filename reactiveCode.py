import time
import ev3dev.ev3 as ev3
from SturdyRobot import *


class Timid(object):
    """This behavior should move forward at a fixed, not-too-fast speed if no object
    is close enough in front of it. When an object is detected, it should stop moving."""

    def __init__(self, robot=None):
        """Set up motors/robot and sensors here"""
        self.robot = robot
        self.us = ev3.UltrasonicSensor("in3")
        self.us.mode = "US-DIST-CM"

    def run(self):
        """One cycle of feedback loop: read sensors, choose movement, set movement."""
        print(self.us.distance_centimeters)
        if not self.robot.is_moving() and self.us.distance_centimeters > 10:
            self.robot.forward(0.3)
        elif self.us.distance_centimeters <= 10:
            self.robot.stop()


class WaryBehavior(object):
    """This is the behavior to move forward until found an object, and move backward if
    that object is getting too close"""

    def __init__(self, robot=None):
        """Set up robot and sensors"""
        self.robot = robot
        self.us = ev3.UltrasonicSensor("in3")
        self.us.mode = "US-DIST-CM"

    def run(self):
        """The robot will run toward until found an object, and try to keep a certain distance
        with that object"""
        if not self.robot.is_moving() and self.us.distance_centimeters > 10:
            self.robot.forward(0.2)
        elif self.us.distance_centimeters <= 5:
            self.robot.backward(0.2)
        elif self.us.distance_centimeters <= 10:
            self.robot.stop()


class ExitCrowdBehavior(object):
    """This behaviour should turn in place when an obstacle is too close. When there is no Obstacle
    it should move forward in that direction."""

    def __init__(self, robot=None):
        """Set up robot and sensors"""
        self.robot = robot
        self.us = ev3.UltrasonicSensor("in3")
        self.us.mode = "US-DIST-CM"

    def run(self):
        """The robot will run toward until found an object, and try to keep a certain distance
        with that object"""
        if not self.robot.is_moving() and self.us.distance_centimeters > 10:
            self.robot.forward(0.2)
        elif self.us.distance_centimeters <= 10:
            while self.us.distance_centimeters <= 15:
                self.robot.turnLeft(0.2)
            self.robot.stop()

class LineFollowing(object):
    """This behavior should follow a black line"""

    def __init__(self, robot=None):
        "Set up the robot and sensors"
        self.robot = robot
        self.colorSensor = ev3.ColorSensor("in2")
        self.colorSensor.mode = "COL-COLOR"

    def run(self):
        """The robot will follow a black line. If it is move out of the line, it will
        turn left and right to find out where is the line"""
        if not self.robot.is_moving() and self.colorSensor.value() == self.colorSensor.COLOR_BLACK:
            self.robot.forward(0.2)
        elif self.colorSensor.value() != self.colorSensor.COLOR_BLACK:
            self.robot.stop()
            # Make the robot go backward a bit before ziggling to find black
            self.robot.backward(0.2, 0.1)

            self.robot.turnLeft(0.1, 0.4)
            if self.colorSensor.value() != self.colorSensor.COLOR_BLACK:
                self.robot.turnRight(0.1, 0.8)



def runBehavior(behavObj, runTime=None):
    """Takes in a behavior object and an optional time to run. It runs
    a loop that calls the run method of the behavObj over and over until
    either the time runs out or a button is pressed."""
    buttons = ev3.Button()
    startTime = time.time()
    elapsedTime = time.time() - startTime
    ev3.Sound.speak("Starting")
    while (not buttons.any()) and ((runTime is None) or (elapsedTime < runTime)):
        behavObj.run()
        # Could add time.sleep here if need to slow loop down
        elapsedTime = time.time() - startTime
    ev3.LargeMotor("outB").stop()
    ev3.LargeMotor("outC").stop()
    ev3.Sound.speak("Done")


if __name__ == '__main__':
    # set up robot object here if using it
    robot = SturdyRobot("teamA")
    timBehav = Timid(robot=robot)  # pass robot object here if need be
    waryBehav = WaryBehavior(robot=robot)
    exitBehav = ExitCrowdBehavior(robot=robot)
    lineFollowBehav = LineFollowing(robot=robot)

    # runBehavior(timBehav)
    # runBehavior(waryBehav)
    # runBehavior(exitBehav)
    runBehavior(lineFollowBehav)

    # add code to stop robot motors
