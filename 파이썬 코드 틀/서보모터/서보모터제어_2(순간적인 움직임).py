#빠르게 왔다갔다하게 만들기

import RPi.GPIO as gpio
import time

servo_pin = 18

gpio.setmode(gpio.BCM)

gpio.setup(servo_pin, gpio.OUT)

pwm = gpio.PWM(servo_pin, 50)
pwm.start(3.0)


#크게크게 바꿔서 빠르게 움직임.(순간이동)
for cnt in range(0, 3):
    pwm.ChangeDutyCycle(3.0)  # 0.6ms == 0도
    time.sleep(1.0)
    pwm.ChangeDutyCycle(12.0)  # 2.4ms == 180도
    time.sleep(1.0)

pwm.ChangeDutyCycle(0.0)

pwm.stop()
gpio.cleanup()