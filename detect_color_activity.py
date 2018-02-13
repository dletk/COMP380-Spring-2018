from SturdyRobot import *

robot = SturdyRobot("A")
cs = ev3.ColorSensor("in2")
cs.mode = 'COL-COLOR'

button = ev3.Button()
#Since cs.color returns an int,make a dict
color_dict = {0:"NO COLOR",
                1:"Black",
                2:"Blue",
                3:"Green",
                4:"Yellow",
                5:"Red",
                6:"White",
                7:"Brown"
                }
while not button.any():
    robot.forward(0.03)
    if cs.color in color_dict.keys():
        ev3.Sound.speak(color_dict[cs.color])
        robot.stop()
        break
    #print("cs color is: ", cs.color)

robot.stop()
