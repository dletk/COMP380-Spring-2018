"""Contains a dictionary to represent the FSM: state is the key, value is ...
a function that checks sensors and takes actions, returning the new state. Other
models are possible."""

import time
import ev3dev.ev3 as ev3


class Timid(object):
    """This behavior should move forward at a fixed, not-too-fast speed if no object
    is close enough in front of it. When an object is detected, it should stop moving."""
    def __init__(self, robot = None):
        """Set up motors/robot and sensors here, set state to 'seeking' and forward
        speed to nonzero"""
        <set up motors and sensors>
        self.FSM = {'seeking': self.updateSeeking,
                    'found': self.updateFound}
        self.state = 'seeking'
        <turn motors on>

    def updateSeeking(self):
        if <object is close>:
            <turn motors off>
            return 'found'
        return None


    def updateFound(self):
        if <object is not close>:
            <turn motors on>
            return 'seeking'
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
        # Could add time.sleep here if need to slow loop down
        elapsedTime = time.time() - startTime
    ev3.Sound.speak("Done")


if __name__ == '__main__':
    # set up robot object here if using it
    timBehav = Timid()  # pass robot object here if need be

    runBehavior(timBehav)

    # add code to stop robot motors

