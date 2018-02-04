import ev3dev.ev3 as ev3
import time

leftMotor = ev3.LargeMotor("outC")
rightMotor = ev3.LargeMotor("outB")
us = ev3.UltrasonicSensor("in3")
gyro = ev3.GyroSensor("in1")

gyro.mode = "GYRO-CAL"
print("====> Calibrated")
time.sleep(3)
gyro.mode = "GYRO-ANG"
us.mode = "US-DIST-CM"

leftMotor.speed_sp = 400
rightMotor.speed_sp = 400

count = 0

def turnRight():
    # global count
    # count += 1
    # Turn right
    rightMotor.speed_sp = -400
    leftMotor.speed_sp = 400
    # 900-1000 is the time to turn exact 90 degree for speed of 400
    # turnTime = 1000
    # if (count % 5) == 0:
    #     turnTime = 1100
    leftMotor.run_forever()
    while True:
        print("====> Gyro: " + str(gyro.value()))
        if abs(gyro.value()) >= 90:
            # Stop the robot
            leftMotor.stop()
            time.sleep(0.1)
            # Calibrate the gyro
            gyro.mode = "GYRO-CAL"
            time.sleep(0.5)
            gyro.mode = "GYRO-ANG"
            gyro.mode = "GYRO-CAL"
            time.sleep(0.5)
            print("=======> Calibrated")
            gyro.mode = "GYRO-ANG"
            break

    rightMotor.speed_sp = 400
    # Resume the run
    leftMotor.run_forever()
    rightMotor.run_forever()


lastTime = time.time()
ev3.Sound.beep()
leftMotor.run_forever()
rightMotor.run_forever()

while True:
    # print(us.distance_centimeters)
    if us.distance_centimeters < 15:
        leftMotor.stop()
        rightMotor.stop()
        ev3.Sound.speak("Obstacle found").wait()
        turnRight()
# while True:
#     # Go ahead for 3 seconds
#     rightMotor.speed_sp = leftMotor.max_speed
#     leftMotor.run_timed(time_sp=3000)
#     rightMotor.run_timed(time_sp=3000)
#     # Turn left
#     leftMotor.wait_until_not_moving()
#     rightMotor.speed_sp = -leftMotor.max_speed
#     leftMotor.run_timed(time_sp=3000)
#     leftMotor.wait_until_not_moving()
#     ev3.Sound.speak("Sir, I have arrived at the destination").wait()
