import ev3dev.ev3 as ev3


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
            self.leftMotor.run_timed(time_sp=time)
            self.rightMotor.run_timed(time_sp=time)

    def backward(self, speed, time=None):
        # This method will call the forward method with a negative speed
        self.forward(-speed, time)

    def turnLeft(self, speed, time=None):
        # The leftMotor stops while the right is running will make the SturdyRobot turn left
        self.leftMotor.stop()

        # Calculate the speed of right motors
        speedTurnLeft = self.rightMotor.max_speed * speed

        self.rightMotor.speed_sp = speedTurnLeft
        if time is None:
            self.rightMotor.run_forever()
        else:
            self.rightMotor.run_timed(time_sp=time)

    def turnRight(self, speed, time=None):
        # The rightMotor stops while the left is running will make the robot turn right
        self.rightMotor.stop()

        # Calculate the speed of left motors
        speedTurnRight = self.leftMotor.max_speed * speed

        self.leftMotor.speed_sp = speedTurnRight
        if time is None:
            self.leftMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    def curve(self, leftSpeed, rightSpeed, time=None):
        leftSpeed = leftSpeed * self.leftMotor.max_speed
        rightSpeed = rightSpeed * self.rightMotor.max_speed

        self.leftMotor.speed_sp = leftSpeed
        self.rightMotor.speed_sp = rightSpeed

        if time is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time)
            self.rightMotor.run_timed(time_sp=time)

    def zeroPointer(self):
        currentPosition = self.mediumMotor.position
        self.mediumMotor.position_sp = -currentPosition
        self.mediumMotor.speed_sp = self.mediumMotor.max_speed
        self.mediumMotor.run_to_rel_pos()

    def pointerLeft(self, speed=1.0, time=None):
        pass

    def pointerRight(self, speed=1.0, time=None):
        pass

    def pointerTo(self, angle):
        pass
