from gpiozero import Robot, LineSensor
import lgpio
robot = Robot(left=(12,13), right=(10,11)) #left side are pins 16 and 18, right side are pins 38 and 40
left_sensor = LineSensor(17) #pin 11
right_sensor= LineSensor(27) #pin 13

speed = 0.65

def motor_speed():
    while True:
        left_detect  = left_sensor.value
        right_detect = right_sensor.value
        ## Stage 1
        if left_detect == 0 and right_detect == 0:
            left_mot = 1
            right_mot = 1
        ## Stage 2
        elif  left_detect == 0 and right_detect == 1:
            left_mot = -1
        elif  left_detect == 1 and right_detect == 0:
             right_mot = -1
	
        #print(r, l)
        yield (right_mot * speed, left_mot * speed)

robot.source = motor_speed()
