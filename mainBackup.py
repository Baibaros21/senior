import SensorData
import RPi.GPIO as GPIO
import time
import PubSub 
import Sensor
import Ultrasonic 
import AccelGyro 
import requests 
import numpy as np
import cv2


BIKE_ID = "502a407c-1c95-49e8-af59-0f90fa4873f0"
pubsub = PubSub.MQTTPubSub() 
data = SensorData.SensorData(BIKE_ID)
GPIO.setmode(GPIO.BCM)

trig_pin=19
echo_pin=20
UltrasonicConnections=[trig_pin, echo_pin]
UltrasonicLocation="front"
ultrasonic=Ultrasonic.UltrasonicSensor(connections=UltrasonicConnections, location=UltrasonicLocation)

busNum=1
address = 0x68       #This is the address value read via the i2cdetect command
#Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
AccelGyroConnections=[busNum, address, power_mgmt_1, power_mgmt_2]
accelGyro=AccelGyro.AccelGyroSensor(connections=AccelGyroConnections)


#comment the following lines to test publishing without driver input without 
#Make sure to set pubsub.start==True
#pubsub.start==True

pubsub.subscribe(data.bikeid)
print("waiting for Driver to start the trip...")
while(pubsub.start==False):
    pass

if (ultrasonic.register()==False):
    print (ultrasonic.error())
else:

    while (pubsub.start==True):

        data.distance=ultrasonic.read()
        print (data.distance)
        if (accelGyro.register()==False):
            print(accelGyro.error())
        else: 
            data.accelGyro = accelGyro.read()
            print(data.accelGyro)
        pubsub.publish(data.bikeid,data.to_string())
        time.sleep(1)
        #print(distance)
    print("Driver Ended the Trip\n Disconnecting.....")
    pubsub.disconnect()

        
        
