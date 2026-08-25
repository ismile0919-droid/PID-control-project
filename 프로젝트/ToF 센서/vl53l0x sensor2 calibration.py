import board
import busio
import adafruit_vl53l0x

i2c=busio.I2C(board.SCL,board.SDA)

sensor2=adafruit_vl53l0x.VL53L0X(i2c)
try :
    distance2=0

    for i in range(2):
        distance2=distance2+sensor2.range

    distance2=distance2/2    
        

except KeyboardInterrupt:
    print("Exit")
except Exception as e:
    print("Error")