import ev3dev.ev3 as ev3

bttn = ev3.Button()

leftLED = ev3.Leds.LEFT

while True:
    leftLED.set_color(leftLED, ev3.Leds.RED)
