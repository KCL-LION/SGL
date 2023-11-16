from gpiozero import Robot, Linesensor
from time import sleep

robot = Robot(left=(12,13),right=(10,11))
left_sensor = Linesensor(17)
right_sensor = Linesensor(27)

speed=0.65
def motor_speed():
    while True:
        left_detect = int(sensor.value)
        right_detect = int(sensor.value)
        ##case 1
        if left_detect ==0 and right_detect == 0:
            left_mot=1
            right_mot=1
        ##case 2
        if left_detect==0 and right_detect==1:
            left_mot=-1
        if left_detect==1 and right_detect==0:
            right_mot=-1
        #print sensor value
        yield(right_mot*speed,left_mot*speed)
    robot.source=motor_speed()
