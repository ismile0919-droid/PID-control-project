import RPi.GPIO as gpio
import time

servo_pin = 18
gpio.setmode(gpio.BCM)
gpio.setup(servo_pin, gpio.OUT)

pwm = gpio.PWM(servo_pin, 50)
pwm.start(0)

def servo_write(value):
    pulse_width = 1.0 + (value / 180)
    #펄스폭은 1.0ms~2.0ms의 값을 가진다.
    #제어값(0~180) = 1.0ms + 제어값 / 180 이렇게 반환.

    duty_cycle = (pulse_width / 20) * 100
    #

    pwm.ChangeDutyCycle(duty_cycle)

servo_write(90)
time.sleep(1)

servo_write(180)
time.sleep(2)

servo_write(0)
time.sleep(2)

servo_write(90)

pwm.stop()
gpio.cleanup()