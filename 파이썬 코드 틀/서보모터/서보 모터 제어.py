#서보모터의 주파수는 50Hz의 PWM신호를 사용하는 것이 표준. 따라서 주기는 20ms이다.
#툭정 듀티비에 대해 특정 각도로 회전하라는 것이 정해져 있다. 
#5%=0도, 7.5%=90도, 10%=180도.

import RPi.GPIO as gpio
import time

servo_pin=18

gpio.setmode(gpio.BCM)

gpio.setup(servo_pin,gpio.OUT)

pwm=gpio.PWM(servo_pin,50) #서보모터 규격인 50Hz 주파수로 PWM 객체를 생성.

#신호를 high나 low로 고정하는 것이 아니라 계속 바꿔주기 위해서 pwm객체를 만드는 것임.
#pwm객체를 이용하면 changedutycycle 명령어를 통해 내부 값에 바로 접근해서 조정할 수 있다.

pwm.start(3.0) #저가형 모터의 오차때문에 3%로 설정. 모터가 떨린다면 3.1,3.2로 설정해보자.
#듀티비를 3%로 설정하여 모터를 0도로 정렬.
time.sleep(2.0) #돌아갈 수 있도록 2초간 대기
pwm.ChangeDutyCycle(0.0) #목표 각도에 도착했으면 정지.(대기시에도 떨림 발생 가능하기때문에 정지시켜줌)

pwm.stop()
gpio.cleanup()
