import RPi.GPIO as GPIO
import Ultrasonic 
import AccelGyro 
from reporter import Reporter
from Impact import FSR
import numpy as np
import cv2
from ArducamVideoFINAL import ArduCam

if __name__ == "__main__":
    BIKE_ID = "502a407c-1c95-49e8-af59-0f90fa4873f0"
   
    reporter  = Reporter()#This classs will be used for all types of reporting either warning, data uplaoding or add data to trip class
    GPIO.setmode(GPIO.BCM)


#intiaizng sensors and camera 
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

    #intializing FSR
    FSR_PIN = 22 #not sure please check correct pin number
    location = "left-side"
    fsr = FSR(FSR_PIN, location,reporter)

    #intializing camera 
    arducam = ArduCam("front")
    arducam.register()

    print("waiting for Driver to start the trip...")
    # to override the wating command, uncomment the following line 
    #reporter.pubsub.start = True
    reporter.waitForTripStart # waiting until the driver starts the trip 

    #Registeration of the sensors. Requires further alteration 
    if (ultrasonic.register()==False):
        print (ultrasonic.error()) 
    fsr.register()
    fsr.read()
    if (accelGyro.register()==False):
        print(accelGyro.error())

    #starts reading and processing. Each sensors has its own processor function which returns the data and the processing results
    while(reporter.isTripDone==False): 

        arducam.record()

        #Each of the processing results are stored in json object.
        ultraData,ultraWarning = ultrasonic.process
        ultrasonicreading = {"data":ultraData, "warning":ultraWarning}

        accelGyrodata,accelGyroWarning = accelGyro.process
        accelGyroreading = {"data":accelGyrodata, "warning":accelGyroWarning}

        #The impact sensor has ISR which will directly report an impact tot he mobile application and stop the trip 
        impactData = fsr.process
        impactreading = {"data":impactData}
        #send the data and processing results to reporter to identify whither warnings should be sent or not
        reporter.porcess(ultrasonicreading,accelGyroreading,impactreading)
        
        #we can set a timer to upload the data every x minutes



