import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)
p = gpio.PWM(18, 50)

print("number = 7.5")
time.sleep(3.0)
p.start(7.5)
time.sleep(3.0)
test=7.1

for i in range(0,10):
    print("number",test)
    time.sleep(3.0)
    p.ChangeDutyCycle(test)
    test = test + 0.1

gpio.cleanup()