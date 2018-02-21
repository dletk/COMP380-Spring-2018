import ev3dev.ev3 as ev3
import time


class SturdyRobot(object):
    """The class to create a manager for robot"""

    # ---------------------------------------------------------------------------
    # Constants for the configDict
    LEFT_MOTOR = 'left-motor'
    RIGHT_MOTOR = 'right-motor'
    MEDIUM_MOTOR = 'medium-motor'
    LEFT_TOUCH = 'left-touch'
    RIGHT_TOUCH = 'right-touch'
    ULTRA_SENSOR = 'ultra-sensor'
    COLOR_SENSOR = 'color-sensor'
    GYRO_SENSOR = 'gyro-sensor'

    # ---------------------------------------------------------------------------

    def __init__(self, name, configDict=None):
        """ Take the configuration of the robot and set up the robot"""
        super(SturdyRobot, self).__init__()
        self.name = name

        # self.leftMotorPort = leftMotorPort
        # self.rightMotorPort = rightMotorPort
        # self.mediumMotorPort = mediumMotorPort

        self.leftMotor = None
        self.rightMotor = None
        self.mediumMotor = None
        self.leftTouch = None
        self.rightTouch = None
        self.ultraSensor = None
        self.colorSensor = None
        self.gyroSensor = None

        if configDict is not None:
            # Call the method to set up the setup sensors and motors
            self.setupSensorsMotors(configDict)
        if self.leftMotor is None:
            self.leftMotor = ev3.LargeMotor("outC")
        if self.rightMotor is None:
            self.rightMotor = ev3.LargeMotor("outB")
        if self.mediumMotor is None:
            self.mediumMotor = ev3.MediumMotor("outD")

        # Reset the motor to the default setting
        self.reset()
        # Make sure the motors stop at exact position
        self.mediumMotor.stop_action = "hold"
        self.rightMotor.stop_action = "hold"
        self.leftMotor.stop_action = "hold"

    def setupSensorsMotors(self, configDict):
        for item in configDict:
            port = configDict[item]
            if item == self.LEFT_MOTOR:
                self.leftMotor = ev3.LargeMotor(port)
            elif item == self.RIGHT_MOTOR:
                self.rightMotor = ev3.LargeMotor(port)
            elif item == self.MEDIUM_MOTOR:
                self.mediumMotor = ev3.MediumMotor(port)
            elif item == self.LEFT_TOUCH:
                self.leftTouch = ev3.TouchSensor(port)
            elif item == self.RIGHT_TOUCH:
                self.rightTouch = ev3.TouchSensor(port)
            elif item == self.ULTRA_SENSOR:
                self.ultraSensor = ev3.UltrasonicSensor(port)
            elif item == self.GYRO_SENSOR:
                self.gyroSensor = ev3.GyroSensor(port)
            elif item == self.COLOR_SENSOR:
                self.colorSensor = ev3.ColorSensor(port)
            else:
                print("Error while setting the item: " + item)

    def reset(self):
        self.rightMotor.reset()
        self.leftMotor.reset()
        self.mediumMotor.reset()

    def setupTouchSensor(self, side, port):
        if item == self.LEFT_TOUCH:
            self.leftTouch = ev3.TouchSensor(port)
        elif item == self.RIGHT_TOUCH:
            self.rightTouch = ev3.TouchSensor(port)
        else:
            print("Incorrect value for side")

    def setGyroSensor(self, port):
        self.gyroSensor = ev3.GyroSensor(port)

    def setUltrasonicSensor(self, port):
        self.ultraSensor = ev3.UltrasonicSensor(port)

    def setMotors(self, side, port):

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
            self.leftMotor.run_timed(time_sp=time * 1000)
            self.rightMotor.run_timed(time_sp=time * 1000)
            self.wait_until_not_moving()

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
            self.rightMotor.run_timed(time_sp=time * 1000)
            self.leftMotor.run_timed(time_sp=time * 1000)
            self.wait_until_not_moving()

    def turnRight(self, speed, time=None):
        # Calculate the speed of left motors
        speedTurnRight = self.leftMotor.max_speed * speed

        self.leftMotor.speed_sp = speedTurnRight
        self.rightMotor.speed_sp = -speedTurnRight
        if time is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time * 1000)
            self.rightMotor.run_timed(time_sp=time * 1000)
            self.wait_until_not_moving()

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

        # Stop the medium motor as well
        self.mediumMotor.stop()

    def curve(self, leftSpeed, rightSpeed, time=None):
        leftSpeed = leftSpeed * self.leftMotor.max_speed
        rightSpeed = rightSpeed * self.rightMotor.max_speed

        self.leftMotor.speed_sp = leftSpeed
        self.rightMotor.speed_sp = rightSpeed

        if time is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            self.leftMotor.run_timed(time_sp=time * 1000)
            self.rightMotor.run_timed(time_sp=time * 1000)
            self.wait_until_not_moving()

    def zeroPointer(self):
        currentPosition = self.mediumMotor.position % 360
        if currentPosition != 0:
            if currentPosition <= 180:
                self.mediumMotor.position_sp = -currentPosition
            else:
                self.mediumMotor.position_sp = 360 - currentPosition
            self.mediumMotor.speed_sp = self.mediumMotor.max_speed
            self.mediumMotor.run_to_rel_pos()
            self.mediumMotor.wait_until_not_moving()
            # TODO: We should be able to set the position to 0 here, but unfortunately not
        time.sleep(0.5)
        self.mediumMotor.reset()

    def pointerLeft(self, speed=1.0, time=None):
        # Calculate the speed of the motor
        speedLeft = - (speed * self.mediumMotor.max_speed)
        self.mediumMotor.speed_sp = speedLeft

        if time is None:
            self.mediumMotor.run_forever()
        else:
            self.mediumMotor.run_timed(time_sp=time * 1000)
            self.mediumMotor.wait_until_not_moving()

    def pointerRight(self, speed=1.0, time=None):
        self.pointerLeft(-speed, time)

    def pointerTo(self, angle):
        if angle <= 360 and angle >= 0:
            self.mediumMotor.speed_sp = 0.5 * self.mediumMotor.max_speed
            self.mediumMotor.position_sp = angle
            self.mediumMotor.run_to_rel_pos()

    def wait_until_not_moving(self):
        self.leftMotor.wait_until_not_moving()
        self.rightMotor.wait_until_not_moving()

    def is_moving(self):
        return self.leftMotor.is_running and self.rightMotor.is_running
