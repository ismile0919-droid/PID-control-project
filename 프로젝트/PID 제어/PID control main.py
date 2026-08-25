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
xshut1=digitalio.DigitalInOut(board.D20)
xshut2=digitalio.DigitalInOut(board.D21)

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

try:
    test1 = None

    if sensor1.data_ready:
        test1=sensor1.distance*10
        sensor1.clear_interrupt()
    elif test1 is None:
         print("VL53L1X ranging error")
         gpio.cleanup()
         sys.exit()
    else:
        print("VL53L1X sensor error")
        gpio.cleanup()
        sys.exit()

    try:
        test2=None
        test2=sensor2.range

        if test2 is None or test2<0 or test2>2000:
             print("VL53L0X ranging error")

    except Exception as e:
         print("VL53L0X sensor error", e)

    print(
            "sensor 1(VL53L1X) : ", test1, "mm"
            "sensor 2(VL53L0X) : ", test2, "mm"
            "Address setting is finished")

    time.sleep(0.1)
except KeyboardInterrupt:
    print("\n EXIT")


time.sleep(1.0)


#PID control main loop
try:
    time.sleep(0.03) #vl53l1x data ready(timing budget=20ms)

    servo_pin = 18                  #servo motor
    gpio.setmode(gpio.BCM)
    gpio.setup(servo_pin, gpio.OUT)
    pwm=gpio.PWM(servo_pin,50)
    pwm.start(7.5)
    max_duty_span = 2.5

    miss_count1=0
    distance1=None
    distance2_prev=None

    while True:



        #vl53l0x
        raw_distance2=sensor2.range
        if raw_distance2 is None or raw_distance2<0 or raw_distance2 >=2000:
             print("VL53L0X sensor error")
             break
        
        if distance2_prev is None:
             distance2=raw_distance2
        else:
             distance2 = (distance2_prev+raw_distance2)/2
        distance2_prev = raw_distance2



        #vl53l1x
        if sensor1.data_ready:
             new_distance1 = sensor1.distance
             sensor1.clear_interrupt()
             if new_distance1 is None or new_distance1 <0 or new_distance1 >1000:
                  miss_count1+=1
             else:
                  distance1=new_distance1
                  miss_count1=0
        else:
             miss_count1 +=1

        if miss_count1>=3:
             print("VL53L1X seneor error")
             break

        if distance1 is None:
            continue



        #p control
        Kp=1

        deviation = distance1-distance2/10
        deviation = max(-50, min(50, deviation))
    

        if abs(deviation) < 1.0:
            pwm.ChangeDutyCycle(7.5)
            continue
        else:
             duty_p = Kp*(deviation/50)*2.5
             duty_p = max(-2.5, min(2.5, duty_p))

        Ut = 7.5 + (Kp*duty_p )

        pwm.ChangeDutyCycle(Ut)



        #Ki=1
        #integralerror = 

        
        #dutycycle range =  left high 0 ~ 50(stop) ~ 100 Right high
        #time.sleep(0.02)



except KeyboardInterrupt:
     print("EXIT")
except Exception as e:
     print("ERROR",e)

finally:
    sensor1.stop_ranging()
    xshut1.deinit()
    xshut2.deinit()
    pwm.stop()
    gpio.cleanup()
    
