import RPi.GPIO as gpio
import time

servo_pin =18
SERVO_MAX_DUTY =12
SERVO_MIN_DUTY=3

gpio.setmode(gpio.BCM)
gpio.setup(servo_pin,gpio.out)

servo=gpio.PWM(servo_pin,50)
servo.start(0)

def servo control