import RPi.GPIO as GPIO
import time

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

def set_motors_pwm(pwm_value):
    pwm_right.ChangeDutyCycle(pwm_value)  # Convert 0-255 range to 0-100
    pwm_left.ChangeDutyCycle(pwm_value)

def test_motors():
    pwm_right.ChangeDutyCycle(75)
    pwm_left.ChangeDutyCycle(75)
    GPIO.output(R_EN_RIGHT,GPIO.HIGH)
    GPIO.output(R_EN_LEFT,GPIO.HIGH)
    GPIO.output(L_EN_RIGHT,GPIO.HIGH)
    GPIO.output(L_EN_LEFT,GPIO.HIGH)

#################################################

if __name__=="__main__":
    try:
        stop_time = time.time() + 10
        while time.time() < stop_time:
            print("Test motors. ETA 10s:")
            # pwm_right.ChangeDutyCycle(75)
            # pwm_left.ChangeDutyCycle(75)
            # GPIO.output(R_EN_RIGHT,GPIO.HIGH)
            # GPIO.output(R_EN_LEFT,GPIO.HIGH)
            # GPIO.output(L_EN_RIGHT,GPIO.HIGH)
            # GPIO.output(L_EN_LEFT,GPIO.HIGH)
            test_motors()
            time.sleep(10)
            print("Stopped after 10 seconds!")

    except KeyboardInterrupt:
        print("Keyboard Interrupt!")

    except:
        print("Other error occured!")

    finally:
        GPIO.cleanup()
