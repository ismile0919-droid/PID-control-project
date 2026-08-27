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


time.sleep(1.0)


#PID control main loop
try:
    time.sleep(0.03) #vl53l1x data ready(timing budget=20ms)

    servo_pin = 18                  #servo motor
    gpio.setmode(gpio.BCM)
    gpio.setup(servo_pin, gpio.OUT)
    pwm=gpio.PWM(servo_pin,50)
    pwm.start(7.5)

    miss_count1=0
    distance1=None
    distance2_prev=None

    #d control
    prev_deviation = 0.0
    prev_time=time.time()

    while True:
        #vl53l0x
        raw_distance2=sensor2.range
        if raw_distance2 is None or raw_distance2<0 or raw_distance2 >=2000:
             print("VL53L0X sensor error 2")
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
             print("VL53L1X seneor error 2")
             break

        if distance1 is None:
            continue



        #p control
        Kp=0.6

        deviation = distance1-distance2/10 #cm
        deviation = max(-5, min(5, deviation))

        if abs(deviation) <= 1.0:
            pwm.ChangeDutyCycle(7.2)
            continue
        elif deviation < 0:
             duty_delta = Kp*(abs(deviation/5))*2.6
             duty_p = 7.4 + min(2.5,duty_delta)
        else:
             duty_delta = Kp*(abs(deviation)/5)*2.0
             duty_p = 7.0 - min(2.2,duty_delta)
     


        #D control
        Kd=0.05
        current_time=time.time()

        dt=current_time-prev_time
        prev_time = current_time

        if dt<=0 or dt > 0.2:
             dt=0.333

        derivation = (deviation-prev_deviation)/dt
        prev_deviation = deviation

        derivation = max(-50, min(50, derivation))
        duty_d = Kd*derivation

          #LPF

        Ut = max(4.5, min(10.0, duty_p + duty_d))
        Ut = duty_p + duty_d
        print("D1:", distance1, "D2:", distance2/10,
              "error:", deviation,"Ut:", Ut)
        pwm.ChangeDutyCycle(Ut)



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