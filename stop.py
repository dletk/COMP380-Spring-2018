import ev3dev.ev3 as ev3

leftMotor = ev3.LargeMotor("outC")
rightMotor = ev3.LargeMotor("outB")

leftMotor.stop()
rightMotor.stop()
