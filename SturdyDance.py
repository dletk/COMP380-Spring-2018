from SturdyRobot import *
import time as t
robot = SturdyRobot("A")
ev3.Sound.set_volume(10)

starSong = [('C4', 'q'), ('C4', 'q'), ('G4', 'q'), ('G4', 'q'),
            ('A4', 'q'), ('A4', 'q'), ('G4', 'h'),
            ('F4', 'q'), ('F4', 'q'), ('E4', 'q'), ('E4', 'q'),
            ('D4', 'q'), ('D4', 'q'), ('C4', 'h') ]


#time.sleep(1.0)

def playSong(song):
    ev3.Sound.play_song(song)


def dance(robot,speed,time=None):
    playSong(starSong)
    #robot.curve(speed,2,1)#trying to go in s curve
    t.sleep(0.5)
    #robot.curve(2,speed,1)
    t.sleep(0.5)
    robot.forward(speed,time)# go onto the stage
    t.sleep(1.0)
    robot.turnLeft(0.5,2.5)#spin around show your stuff!
    t.sleep(0.5)
    robot.turnRight(0.5,2.5)
    t.sleep(0.5)
    robot.backward(speed,time)
    t.sleep(0.5)
    robot.pointerLeft(speed,2.5)
#ev3.Sound.speak("I love goats!").wait()
#time.sleep(1.0)
dance(robot,1,1)
