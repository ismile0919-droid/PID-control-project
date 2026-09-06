import sys
import time
import board
import busio
import digitalio
import RPi.GPIO as gpio
import adafruit_vl53l0x
import adafruit_vl53l1x


#i2c
i2c=board.I2C()

#xshut pin
xshut1=digitalio.DigitalInOut(board.D21)
xshut2=digitalio.DigitalInOut(board.D20)

xshut1.switch_to_output(value=False)
xshut2.switch_to_output(value=False)

time.sleep(0.1)


#sensor1=vl53l1x---------------------------

xshut1.value=True
time.sleep(0.1)
sensor1=adafruit_vl53l1x.VL53L1X(i2c)
sensor1.set_address(0x30)
sensor1.distance_mode = 1
sensor1.timing_budget = 20
sensor1.start_ranging()

#sensor2=vl53l0x----------------------------

xshut2.value=True
time.sleep(0.1)
sensor2=adafruit_vl53l0x.VL53L0X(i2c)



print("Dual Sensor / sensor1=VL53L1X / sensor2=VL53L0X / TEST")
print("detect test distance")
print("\n")

try:
     for i in range(0,10):
        test1 = None
        time.sleep(0.1)
    
        if sensor1.data_ready:
             test1=sensor1.distance
             test1=test1 * 10
             sensor1.clear_interrupt()
        elif test1 is None:
            print("VL53L1X ranging error")
            gpio.cleanup()
            sys.exit()
        else:
            print("VL53L1X sensor error 1")
            gpio.cleanup()
            sys.exit()

        try:
            test2=None
            test2=sensor2.range

            if test2 is None or test2<0 or test2>2000:
                 print("VL53L0X ranging error")

        except Exception as e:
             print("VL53L0X sensor error 1", e)

        print(
            "sensor 1(VL53L1X) : ", test1, "mm"
            "\nsensor 2(VL53L0X) : ", test2, "mm"
            "\nAddress setting is finished")

        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n EXIT")