from SturdyRobot import *
import random

SPEED_MOVEMENT = 0.4
SPEED_TURN = 0.1
DISTANCE_TO_WALL = 20


def findLight():
    # Set the current heaiding of the robot
    robot.setHeading()
    # ------ Variables to store the maximum light intensity and its angle
    max_ambience_intensity = -1
    max_ambience_turn_count = 0

    # Turn around and gather the ambient light intensity
    turn_count = 0
    robot.readAmbient()  # This call is used to set the mode of color sensor
    heading = robot.readHeading()
    print("HEADING BEFORE: ", heading)
    while heading <= 330:
        # Check to see whether there is a new max ambience intensity found
        current_ambience_intensity = robot.readAmbient()
        print(current_ambience_intensity)
        if current_ambience_intensity > max_ambience_intensity:
            max_ambience_intensity = current_ambience_intensity
            max_ambience_turn_count = turn_count

        # Keep turning
        robot.turnRight(SPEED_TURN, 0.2)
        turn_count += 1
        heading = robot.readHeading()

    # After turn 1 circle, stop the robot, set the heading to current heading
    robot.stop()
    robot.setHeading()
    print("===> Set heading: ", robot.readHeading())

    # Turn the robot back to the location where it found the max ambience
    # Because the robot stops at 330 degree, we turn 3 more times to make it back to origin
    # Each of our turn is approximately 10 degrees
    for i in range(max_ambience_turn_count + 3):
        robot.turnRight(SPEED_TURN, 0.2)

    robot.stop()
    # 7 is the thresh hold of the exit lighting
    if max_ambience_intensity >= 6:
        robot.forward(SPEED_MOVEMENT, 3)
        return True
    else:
        robot.forward(SPEED_MOVEMENT, 0.5)
        return False


def comfortZone():
    """Method to find the comfort zone for the robot to begin measure ambience"""
    # If the robot is too close with a wall in front, or if it is touching the wall
    if robot.readDistance() < DISTANCE_TO_WALL or robot.readTouch()[0] == 1:
        robot.backward(SPEED_MOVEMENT, 0.5)
        return False

    # Check whether the robot is too close to a wall on the left
    robot.pointerLeft(time=0.1)
    if robot.readDistance() < DISTANCE_TO_WALL:
        robot.turnRight(SPEED_MOVEMENT, 0.2)
        robot.forward(SPEED_MOVEMENT, 0.5)
        return False

    # Check whether the robot is too close to a wall on the right
    robot.zeroPointer()
    robot.pointerTo(90)
    if robot.readDistance() < DISTANCE_TO_WALL:
        robot.turnLeft(SPEED_MOVEMENT, 0.2)
        robot.forward(SPEED_MOVEMENT, 0.5)
        return False

    robot.zeroPointer()
    return True


if __name__ == '__main__':
    robot = SturdyRobot("A")
    ev3.Sound.beep()
    robot_out = False
    while not robot_out:
        while comfortZone():
            if findLight():
                robot_out = True
                break

    starSong = [('C4', 'q'), ('C4', 'q'), ('G4', 'q'), ('G4', 'q'),
                ('A4', 'q'), ('A4', 'q'), ('G4', 'h'),
                ('F4', 'q'), ('F4', 'q'), ('E4', 'q'), ('E4', 'q'),
                ('D4', 'q'), ('D4', 'q'), ('C4', 'h')]
    ev3.Sound.play_song(starSong).wait()
