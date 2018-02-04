import ev3dev.ev3 as ev3

mMotor = ev3.MediumMotor("outD")

mMotor.speed_sp = 400
mMotor.stop_action = "hold"
mMotor.position_sp = 90

ev3.Sound.set_volume(30)

for i in range(12):
    mMotor.run_to_rel_pos()
    mMotor.wait_until_not_moving()
    mMotor.run_to_rel_pos()
    mMotor.wait_until_not_moving()
    ev3.Sound.beep().wait()
mMotor.stop()
