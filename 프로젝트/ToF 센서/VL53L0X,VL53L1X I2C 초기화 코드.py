import time
import board
import busio
import digitalio
import adafruit_vl53l0x
import adafruit_vl53l1x

#i2c
i2c=board.I2C()

#xshut pin
xshut1=digitalio.DigitalInOut(board.20)
xshut2=digitalio.DigitalInOut(board.21)

xshut1.switch_to_output(value=False)
xshut2.switch_to_output(value=False)

time.sleep(0.1)


#sensor1=vl53l1x---------------------------

xshut1.value=True
time.sleep(0.1)
sensor1=adafruit_vl53l1x.VL53L1X(i2c)
sensor1.set_address(0x30)
sensor1.start_ranging()

#sensor2=vl53l0x----------------------------

xshut2.value=True
time.sleep(0.1)
sensor2=adafruit_vl53l0x.VL53L0X(i2c)



print("Dual Sensor / sensor1=VL53L1X / sensor2=VL53L0X / TEST")

print("detect test distance")

try:
    while True:
        if sensor1.data_ready:
            distance1=sensor1.distance*10
            sensor1.clear_interrupt()
        else:
            distance=None

        distance2=sensor2.range

        print(
            "sensor 1(VL53L1X) : ", distance1, "mm"
            "sensor 2(VL53L0X) : ", distance2, "mm"
        )

        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n Finish")

finally:
    sensor1.stop_ranging()
    xshut1.deinit()
    xshut2.deinit()


