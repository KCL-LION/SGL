import RPi.GPIO as GPIO
from time import sleep
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # using gpio pins
GPIO.setwarnings(False)
 
# Motor GPIO Pins
LEFT_MOTOR_FORWARD = 12
LEFT_MOTOR_BACKWARD = 18
RIGHT_MOTOR_FORWARD = 19
RIGHT_MOTOR_BACKWARD = 13

# Line Sensor GPIO Pins
LEFT_SENSOR_PIN = 17
RIGHT_SENSOR_PIN = 27 

# Setup Motor Pins
GPIO.setup(LEFT_MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_MOTOR_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_BACKWARD, GPIO.OUT)

# Setup Sensor Pins
GPIO.setup(LEFT_SENSOR_PIN, GPIO.IN)
GPIO.setup(RIGHT_SENSOR_PIN, GPIO.IN)

# PWM Setup
PWM_FREQUENCY = 5000  # Frequency in Hz
LEFT_PWM_FORWARD = GPIO.PWM(LEFT_MOTOR_FORWARD, PWM_FREQUENCY)
LEFT_PWM_BACKWARD = GPIO.PWM(LEFT_MOTOR_BACKWARD, PWM_FREQUENCY)
RIGHT_PWM_FORWARD = GPIO.PWM(RIGHT_MOTOR_FORWARD, PWM_FREQUENCY)
RIGHT_PWM_BACKWARD = GPIO.PWM(RIGHT_MOTOR_BACKWARD, PWM_FREQUENCY)

LEFT_PWM_FORWARD.start(0)
LEFT_PWM_BACKWARD.start(0)
RIGHT_PWM_FORWARD.start(0)
RIGHT_PWM_BACKWARD.start(0)

# PID coefficients
Kp = 0.4
Ki = 0.33
Kd = 0.05

# PID variables
previous_error = 0
integral = 0

def set_motor_speed(left_speed, right_speed):
    # Ensure the speed values are within 0-100%
    left_speed = max(0, min(25, left_speed))
    right_speed = max(0, min(25, right_speed))

    if left_speed > 0:
        LEFT_PWM_FORWARD.ChangeDutyCycle(left_speed)
        LEFT_PWM_BACKWARD.ChangeDutyCycle(0)
    else:
        LEFT_PWM_FORWARD.ChangeDutyCycle(0)
        LEFT_PWM_BACKWARD.ChangeDutyCycle(-left_speed)

    if right_speed > 0:
        RIGHT_PWM_FORWARD.ChangeDutyCycle(right_speed)
        RIGHT_PWM_BACKWARD.ChangeDutyCycle(0)
    else:
        RIGHT_PWM_FORWARD.ChangeDutyCycle(0)
        RIGHT_PWM_BACKWARD.ChangeDutyCycle(-right_speed)

def read_line_sensors():
    return GPIO.input(LEFT_SENSOR_PIN), GPIO.input(RIGHT_SENSOR_PIN)

try:
    while True:
        left_sensor, right_sensor = read_line_sensors()

        # Error calculation for PID
        error = left_sensor - right_sensor
        integral +=  error
        derivative = error - previous_error
        
        # PID output
        pid = Kp * error #+ Ki * integral + Kd * derivative
        previous_error = error

        # Motor speed control
        base_speed = 5
        set_motor_speed(base_speed + pid, base_speed - pid)

except KeyboardInterrupt:
    # Stop the robot safely
    set_motor_speed(0, 0)
    GPIO.cleanup()
