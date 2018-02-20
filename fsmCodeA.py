"""Contains the most primitive version of the FSM: state is a string held in a variable,
and it's just a big if statement."""

import time
import ev3dev.ev3 as ev3
from SturdyRobot import *

class Timid(object):
    """This behavior should move forward at a fixed, not-too-fast speed if no object
    is close enough in front of it. When an object is detected, it should stop moving."""
    def __init__(self, robot = None):
        """Set up motors/robot and sensors here, set state to 'seeking' and forward
        speed to nonzero"""
        self.robot = robot
        self.us = ev3.UltrasonicSensor("in3")
        self.us.mode = "US-DIST-CM"
        self.state = 'seeking'
        self.robot.forward(0.3)#<turn motors on>

    def run(self):
        """Updates the FSM by reading sensor data, then choosing based on the state"""
        if self.state == 'seeking' and self.us.distance_centimeters <= 10:
            self.state = 'found'
            self.robot.stop()#<turn motors off>
        elif self.state == 'found' and self.us.distance_centimeters > 10:
            self.state = 'seeking'
            self.robot.forward(0.3)

class WaryBehavior(object):
    """This is the behavior to move forward until found an object, and move backward if
    that object is getting too close"""

    def __init__(self, robot=None):
        """Set up robot and sensors"""
        self.robot = robot
        self.FSM = {'seeking': self.updateSeeking,
                    'found': self.updateFound}
        self.state = 'seeking'
        self.us = ev3.UltrasonicSensor("in3")
        self.us.mode = "US-DIST-CM"
        self.robot.forward(0.3)

    def updateSeeking(self):
        if self.us.distance_centimeters <= 10:
            self.robot.stop()#<turn motors off>
            return 'found'

        return None

    def updateFound(self):
        if self.us.distance_centimeters > 10:
            self.robot.forward(0.2)
            return 'seeking'
        elif self.us.distance_centimeters <= 5:
            self.robot.backward(0.2)
            return 'found' #but wary
        return None

    def run(self):
        """Updates the FSM by reading sensor data, then choosing based on the state"""
        updateFunc = self.FSM[self.state]
        newState = updateFunc()
        if newState is not None:
            self.state = newState

def runBehavior(behavObj, runTime = None):
    """Takes in a behavior object and an optional time to run. It runs
    a loop that calls the run method of the behavObj over and over until
    either the time runs out or a button is pressed."""
    buttons = ev3.Button()
    startTime = time.time()
    elapsedTime = time.time() - startTime
    ev3.Sound.speak("Starting")
    while (not buttons.any()) and ((runTime is None) or (elapsedTime < runTime)):
        behavObj.run()
        print("Current state is: ", behavObj.state)
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
    runBehavior(waryBehav)

    # add code to stop robot motors
