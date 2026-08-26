import time
import RPi.GPIO as gpio

try:
    servo_pin=18
    gpio.setmode(gpio.BCM)
    gpio.setup(servo_pin,gpio.OUT)
    pwm=gpio.PWM(servo_pin,50)
    time.sleep(0.1)
    pwm.start(7.5)
    time.sleep(0.1)
    pwm.ChangeDutyCycle(6.5)
    time.sleep(0.1)
    pwm.ChangeDutyCycle(7.5)

except KeyboardInterrupt:
    print("Exit")

finally:
    pwm.stop()
    gpio.cleanup()
