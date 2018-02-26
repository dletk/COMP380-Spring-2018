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
    # The default config that the program will use if no config is given
    DEFAULT_CONFIG = {ULTRA_SENSOR: "in3", LEFT_TOUCH: "in2",
                      COLOR_SENSOR: "in4", GYRO_SENSOR: "in1"}

    # ---------------------------------------------------------------------------

    def __init__(self, name, configDict=None):
        """ Take the configuration of the robot and set up the robot
        Default config:
        {SturdyxRobot.ULTRA_SENSOR: "in3", SturdyRobot.LEFT_TOUCH: "in2", SturdyRobot.COLOR_SENSOR: "in4", SturdyRobot.GYRO_SENSOR: "in1"}"""
        super(SturdyRobot, self).__init__()
        self.name = name

        # TODO: Comment on all of the methods

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
        else:
            self.setupSensorsMotors(self.DEFAULT_CONFIG)
        if self.leftMotor is None:
            self.setMotors(self.LEFT_MOTOR, "outC")
        if self.rightMotor is None:
            self.setMotors(self.RIGHT_MOTOR, "outB")
        if self.mediumMotor is None:
            self.setMotors(self.MEDIUM_MOTOR, "outD")

        # Reset the motor to the default setting
        self.reset()
        # Make sure the motors stop at exact position

    def setupSensorsMotors(self, configDict):
        """Method to set up all the sensors and motors based on the input configuration"""
        for item in configDict:
            port = configDict[item]
            if item == self.LEFT_MOTOR:
                self.setMotors(item, port)
            elif item == self.RIGHT_MOTOR:
                self.setMotors(item, port)
            elif item == self.MEDIUM_MOTOR:
                self.setMotors(item, port)
            elif item == self.LEFT_TOUCH:
                self.setupTouchSensor(item, port)
            elif item == self.RIGHT_TOUCH:
                self.setTouchSensor(item, port)
            elif item == self.ULTRA_SENSOR:
                self.setUltrasonicSensor(port)
            elif item == self.GYRO_SENSOR:
                self.setGyroSensor(port)
            elif item == self.COLOR_SENSOR:
                self.setColorSensor(port)
            else:
                print("Error while setting the item: " + item)

    def reset(self):
        """Method to reset all the motors back to their original setting """
        self.rightMotor.reset()
        self.leftMotor.reset()
        self.mediumMotor.reset()

        # Make the stop action of any motor to be hold to maintain its position
        self.rightMotor.stop_action = "hold"
        self.leftMotor.stop_action = "hold"
        self.mediumMotor.stop_action = "hold"

    def setupTouchSensor(self, side, port):
        """Method to set up the touch sensor based on input side and port"""
        if side == self.LEFT_TOUCH:
            self.leftTouch = ev3.TouchSensor(port)
        elif side == self.RIGHT_TOUCH:
            self.rightTouch = ev3.TouchSensor(port)
        else:
            print("Incorrect value for side")

    def setGyroSensor(self, port):
        """Method to set up the gyro sensor"""
        self.gyroSensor = ev3.GyroSensor(port)
        self.setHeading()

    def setUltrasonicSensor(self, port):
        """Method to set up the ultrasonic sensor."""
        self.ultraSensor = ev3.UltrasonicSensor(port)

        # Using continuous measuring mode
        self.ultraSensor.mode = "US-DIST-CM"

    def setColorSensor(self, port):
        """Method to set up the color sensor"""
        self.colorSensor = ev3.ColorSensor(port)

    def setMotors(self, side, port):
        """Method to set up the motors, based on given input side and port"""
        if side == self.LEFT_MOTOR:
            self.leftMotor = ev3.LargeMotor(port)
            self.leftMotor.stop_action = "hold"
        elif side == self.RIGHT_MOTOR:
            self.rightMotor = ev3.LargeMotor(port)
            self.rightMotor.stop_action = "hold"
        elif side == self.MEDIUM_MOTOR:
            self.mediumMotor = ev3.MediumMotor(port)
            self.mediumMotor.stop_action = "hold"
        else:
            print("Your input side is Incorrect")

    def setHeading(self):
        """Set the heading of the robot to the current direction"""
        if self.gyroSensor is not None:
            self.gyroSensor.mode = "GYRO-CAL"
            time.sleep(0.2)
            self.gyroSensor.mode = "GYRO-ANG"
            self.gyroSensor.mode = "GYRO-CAL"
            time.sleep(0.2)
            self.gyroSensor.mode = "GYRO-ANG"
        else:
            print("Cannot find gyro sensor")

    def readTouch(self):
        """Reports the value of both touch sensors, OR just one if only one is connected, OR
        prints an alert and returns nothing if neither is connected."""
        if self.leftTouch is not None and self.rightTouch is not None:
            return self.leftTouch.is_pressed, self.rightTouch.is_pressed
        elif self.leftTouch is not None:
            return self.leftTouch.is_pressed, None
        elif self.rightTouch is not None:
            return None, self.rightTouch
        else:
            print("Warning, no touch sensor connected")
            return None, None

    def readReflect(self):
        """Read the value of reflectance from the color sensor"""
        if self.colorSensor is not None:
            if self.colorSensor.mode != "COL-REFLECT":
                self.colorSensor.mode = "COL-REFLECT"
            return self.colorSensor.reflected_light_intensity
        else:
            print("There is no color sensor set up")

    def readAmbient(self):
        """Read the value of ambient light from the color sensor """
        if self.colorSensor is not None:
            if self.colorSensor.mode != "COL-AMBIENT'":
                self.colorSensor.mode = "COL-AMBIENT"
            return self.colorSensor.ambient_light_intensity
        else:
            print("There is no color sensor set up")

    def readColor(self):
        """Read the value of color from the color sensor"""
        if self.colorSensor is not None:
            if self.colorSensor.mode != "COL-COLOR":
                self.colorSensor.mode = "COL-COLOR"
            return self.colorSensor.color
        else:
            print("There is no color sensor set up")

    def readDistance(self):
        """Read the distance from the robot to the nearest object in the direction
        that the ultrasonic sensor is pointing to"""
        if self.ultraSensor is not None:
            return self.ultraSensor.distance_centimeters
        else:
            print("There is no ultrasonic sensor set up")

    def readHeading(self):
        """Read the heading of the robot from 0 to 359, the origin is set at the
        last time setHeading is called
        The heading is to the right side of the origin
        """
        if self.gyroSensor is not None:
            angle = self.gyroSensor.angle
            if angle < 0:
                # With the current design, the right direction will be negative result
                return abs(self.gyroSensor.angle) % 360
            else:
                # If the angle is positive, that means the robot has turned left
                return (360 * (angle // 360 + 1) - angle) % 360

        else:
            print("Cannot find gyro sensor")

    def forward(self, speed, time=None):
        """Make the robot move forward with the given speed. If there is no given time,
        the robot would move forerver"""
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
        """Make the robot to move backward with the given speed"""
        # This method will call the forward method with a negative speed
        self.forward(-speed, time)

    def turnLeft(self, speed, time=None):
        """Make the robot to turn left inplace with the given speed.
        If there is no given time, the robot keeps turning forever"""
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
        self.mediumMotor.wait_until_not_moving()

    def wait_until_not_moving(self):
        self.leftMotor.wait_until_not_moving()
        self.rightMotor.wait_until_not_moving()

    def is_moving(self):
        """Check whether any of the Large mortor is running"""
        return self.leftMotor.is_running or self.rightMotor.is_running
