sensor.start.ranging()   #거리 측정 시작 코드
sensor.stop.ranging()    #거리 측정 종료 코드
sensor.data_ready        #측정 값이 준비되었는지 확인
sensor.distance          #유효한 거리값 반환(cm단위)
sensor.clear_interrput() #새로운 측정을 위해 상태 초기화

sensor.distance_mode=1   #short거리 모드로 전환. long=2
sensor.timing_budget = 50#50ms수준의 측정 예산을 사용. 15,20,33,50,100,200,500ms 값이 있음. 늘어날 경우 반복성이 좋아짐. 측정거리도 늘어남.




#--------------------------------------------------------
#예제 : if문이 있는 것이 시간지연에 더 좋음.
import time
import board
import adafruit_vl53l1x

i2c = board.I2C()

sensor = adafruit_vl53l1x.VL53L1X(i2c)
sensor.distance_mode = 1
sensor.timing_budget = 20
sensor.start_ranging()

while True:
    if sensor.data_ready:
        distance = sensor.distance

        print(f"Distance: {distance:.1f} cm")

        sensor.clear_interrupt()

    time.sleep(0.01)