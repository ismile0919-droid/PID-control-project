import RPi.GPIO as gpio
import time

servo_pin = 18

gpio.setmode(gpio.BCM)

gpio.setup(servo_pin, gpio.OUT)

pwm = gpio.PWM(servo_pin, 50)
pwm.start(3.0)  # 초기 상태는 0도

for t_high in range(30, 120): #3%~12%=0도~180도(오차고려)
    pwm.ChangeDutyCycle(t_high / 10.0)  # 듀티 비를 3.0 ~ 12.0까지 0.1씩 증가
    time.sleep(0.02)  # 0.02sec delay

pwm.ChangeDutyCycle(3.0)  # 동작이 끝나면 다시 0도로 회전
time.sleep(1.0)
pwm.ChangeDutyCycle(0.0)

pwm.stop()
gpio.cleanup()