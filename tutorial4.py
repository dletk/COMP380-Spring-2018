import ev3dev.ev3 as ev3

rightMotor = ev3.LargeMotor("outB")
leftMotor = ev3.LargeMotor("outC")
us = ev3.UltrasonicSensor("in3")

us.mode = "US-DIST-CM"

leftMotor.speed_sp = 400
rightMotor.speed_sp = 400

count = 0
