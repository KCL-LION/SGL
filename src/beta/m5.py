import RPi.GPIO as GPIO
import time
import socket
import ast 
#################################################

# Pin Definitions:
# Right Motor
R_EN_RIGHT = 24  # was 7 in Arduino
L_EN_RIGHT = 23  # was 4 in Arduino
RPWM_RIGHT = 19  # was 9 in Arduino

# Left Motor
R_EN_LEFT = 16   # was 6 in Arduino
L_EN_LEFT = 26   # was 5 in Arduino
LPWM_LEFT = 13   # was 10 in Arduino

# Setup GPIO
# See similar setup template: https://github.com/KCL-LION/Lions/blob/main/test/TestMotor/test2_PROP.py
# Tidbit on BCM             : https://forums.raspberrypi.com/viewtopic.php?t=7624
GPIO.setmode(GPIO.BCM)

GPIO.setup(R_EN_RIGHT,GPIO.OUT)
GPIO.setup(R_EN_LEFT,GPIO.OUT)
GPIO.setup(L_EN_RIGHT,GPIO.OUT)
GPIO.setup(L_EN_LEFT,GPIO.OUT)

GPIO.setup(RPWM_RIGHT,GPIO.OUT)
GPIO.setup(LPWM_LEFT,GPIO.OUT)

GPIO.output(R_EN_RIGHT,GPIO.LOW)
GPIO.output(R_EN_LEFT,GPIO.LOW)
GPIO.output(L_EN_RIGHT,GPIO.LOW)
GPIO.output(L_EN_LEFT,GPIO.LOW)

pwm_right = GPIO.PWM(RPWM_RIGHT,1000)
pwm_left = GPIO.PWM(LPWM_LEFT,1000)

pwm_right.start(0)
pwm_left.start(0)
#################################################
#UDP server setup
UDP_IP_ADDRESS = "192.168.1.37"  # Listen on all interfaces
UDP_PORT = 1069

serverSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT))

print("UDP server: {} {}".format(socket.gethostbyname(socket.gethostname()), UDP_PORT))

#################################################

def test_motors():
    pwm_right.ChangeDutyCycle(75)
    pwm_left.ChangeDutyCycle(75)
    GPIO.output(R_EN_RIGHT,GPIO.HIGH)
    GPIO.output(R_EN_LEFT,GPIO.HIGH)
    GPIO.output(L_EN_RIGHT,GPIO.HIGH)
    GPIO.output(L_EN_LEFT,GPIO.HIGH)

def drive_motors_based_on_joystick(D35, D34, D35_dir, D34_dir):
     # If joystick sends 0 PWM, stop motors
    if D35 == 0 and D34 == 0:
        pwm_right.ChangeDutyCycle(0)
        pwm_left.ChangeDutyCycle(0)
        return
    # Set the PWM for the motors
    set_motors_pwm(D34, D35)
    # Determine the direction for the right motor based on D34_dir
    if D34_dir == 1:  # positive
        GPIO.output(R_EN_RIGHT, GPIO.HIGH)
        GPIO.output(L_EN_RIGHT, GPIO.LOW)
    else:  # negative
        GPIO.output(R_EN_RIGHT, GPIO.LOW)
        GPIO.output(L_EN_RIGHT, GPIO.HIGH)

    # Determine the direction for the left motor based on D35_dir
    if D35_dir == 1:  # positive
        GPIO.output(R_EN_LEFT, GPIO.HIGH)
        GPIO.output(L_EN_LEFT, GPIO.LOW)
    else:  # negative
        GPIO.output(R_EN_LEFT, GPIO.LOW)
        GPIO.output(L_EN_LEFT, GPIO.HIGH)

def set_motors_pwm(D34_pwm, D35_pwm):
    pwm_right.ChangeDutyCycle(D34_pwm)
    pwm_left.ChangeDutyCycle(D35_pwm)
#################################################

if __name__=="__main__":
    try:
        stop_time = time.time() + 10
        while time.time() < stop_time:
            print("Test motors. ETA 10s:")
            test_motors()
            time.sleep(10)
            print("Stopped after 10 seconds!")
    # For running server and listening for joystick data
        while True:
            # Listen for incoming joystick data
            data, addr = serverSock.recvfrom(1024)
            # Assuming the incoming data format is "[D35, D34, D35_dir, D34_dir]"
            joystick_data_str = data.decode().strip('[]').split(',')
            joystick_data = [int(val.strip()) for val in joystick_data_str]


            # Drive the motors based on joystick data
            drive_motors_based_on_joystick(*joystick_data)

    except KeyboardInterrupt:
        print("Keyboard Interrupt!")

    except:
        print("Other error occured!")

    finally:
        GPIO.cleanup()
