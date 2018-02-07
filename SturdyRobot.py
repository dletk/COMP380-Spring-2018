import ev3dev.ev3 as ev3
import time


class SturdyRobot(object):
    """The class to create a manager for robot"""

    def __init__(self, name,
                 leftMotorPort="outC",
                 rightMotorPort="outB",
                 mediumMotorPort="outD"):
        super(SturdyRobot, self).__init__()
        self.name = name
        self.leftMotorPort = leftMotorPort
        self.rightMotorPort = rightMotorPort
        self.mediumMotorPort = mediumMotorPort

        self.leftMotor = ev3.LargeMotor(self.leftMotorPort)
        self.rightMotor = ev3.LargeMotor(self.rightMotorPort)
        self.mediumMotor = ev3.MediumMotor(self.mediumMotorPort)

        self.reset()
        # Make sure the pointer stop at exact position
        self.mediumMotor.stop_action = "hold"

    def reset(self):
        self.rightMotor.reset()
        self.leftMotor.reset()
        self.mediumMotor.reset()

    def forward(self, speed, time=None):
        # To calculate the speed of the motor, use this formula: speed * max_speed
        # and then set the speed of the motors to that speed
        leftSpeed = speed * self.leftMotor.max_speed
        rightSpeed = speed * self.rightMotor.max_speed

        # Set the speed of both motors
        self.leftMotor.speed_sp = leftSpeed
        self.rightMotor.speed_sp = rightSpeed

        if time is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time*1000)
            self.rightMotor.run_timed(time_sp=time*1000)

    def backward(self, speed, time=None):
        # This method will call the forward method with a negative speed
        self.forward(-speed, time)

    def turnLeft(self, speed, time=None):
        # Calculate the speed of right motors
        speedTurnLeft = self.rightMotor.max_speed * speed

        self.rightMotor.speed_sp = speedTurnLeft
        self.leftMotor.speed_sp = -speedTurnLeft
        if time is None:
            self.rightMotor.run_forever()
            self.leftMotor.run_forever()
        else:
            self.rightMotor.run_timed(time_sp=time*1000)
            self.leftMotor.run_timed(time_sp=time*1000)

    def turnRight(self, speed, time=None):
        # Calculate the speed of left motors
        speedTurnRight = self.leftMotor.max_speed * speed

        self.leftMotor.speed_sp = speedTurnRight
        self.rightMotor.speed_sp = -speedTurnRight
        if time is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time*1000)
            self.rightMotor.run_timed(time_sp=time*1000)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

        # Stop the medium motor as well
        self.mediumMotor.stop()

    def wait_until_not_moving(self):
        self.leftMotor.wait_until_not_moving()
        self.rightMotor.wait_until_not_moving()

    def curve(self, leftSpeed, rightSpeed, time=None):
        leftSpeed = leftSpeed * self.leftMotor.max_speed
        rightSpeed = rightSpeed * self.rightMotor.max_speed

        self.leftMotor.speed_sp = leftSpeed
        self.rightMotor.speed_sp = rightSpeed

        if time is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time*1000)
            self.rightMotor.run_timed(time_sp=time*1000)

    def zeroPointer(self):
        currentPosition = self.mediumMotor.position % 360
        if currentPosition != 0:
            if currentPosition <= 180:
                self.mediumMotor.position_sp = -currentPosition
            else:
                self.mediumMotor.position_sp = 360-currentPosition
            self.mediumMotor.speed_sp = self.mediumMotor.max_speed
            self.mediumMotor.run_to_rel_pos()
            self.mediumMotor.wait_until_not_moving()
            # TODO: We should be able to set the position to 0 here, but unfortunately not

    def pointerLeft(self, speed=1.0, time=None):
        # Calculate the speed of the motor
        speedLeft = - (speed * self.mediumMotor.max_speed)
        self.mediumMotor.speed_sp = speedLeft

        if time is None:
            self.mediumMotor.run_forever()
        else:
            self.mediumMotor.run_timed(time_sp=time*1000)

    def pointerRight(self, speed=1.0, time=None):
        self.pointerLeft(-speed, time)

    def pointerTo(self, angle):
        if angle <= 360 and angle >= 0:
            self.mediumMotor.speed_sp = 0.5 * self.mediumMotor.max_speed
            self.mediumMotor.position_sp = angle
            self.mediumMotor.run_to_rel_pos()
