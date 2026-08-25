#가장 기본적인 파이썬 구조.
import time
import board
import busio
import adafruit_vl5310x

i2c = busio.I2C(board.SCL, board.SDA)
#SDA/SCL을 이용해서 I2C통신을 준비하는 부분

tof = adafruit_vl5310x.VL53LX(i2c)
#센서 객체 생성: 앞서 지정한 I2C버스에 연결되어 있는 VL53L0X센서를 사용하겠다는 의미.

while True:
    distance = tof.range
    #센서가 측정한 현재 거리를 가져오는 부분. mm단위.

    print(distance, "mm")

    time.sleep(0.1)
