from Sensor import Sensor
import RPi.GPIO as GPIO
import time

class UltrasonicSensor(Sensor):
	def __init__(self, connections, location):
		self.name="Ultrasonic Sensor"
		self.trig_pin=connections[0]
		self.echo_pin=connections[1]
		self.location=location
	
	def register(self):
		GPIO.setmode(GPIO.BCM)
		
		GPIO.setup(self.trig_pin, GPIO.OUT)
		GPIO.setup(self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		GPIO.output(self.trig_pin,False)
		count=0
		count2=0
		time.sleep(2)
		while True:
			GPIO.output(self.trig_pin, True)
			time.sleep(0.00001)
    	
			GPIO.output(self.trig_pin, False)
    	
			while GPIO.input(self.echo_pin) == 0:
				a=0
			pulse_start = time.time()
			while GPIO.input(self.echo_pin) == 1:
				if (time.time()-pulse_start>5):
					return False
				
			pulse_end = time.time()
    	
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 1000000/58
			count2=count2+1
			if (distance<700):
				count=count+1
		
			if (count>20):
				GPIO.output(self.trig_pin,False)
				time.sleep(2)
				return True
		
			if (count2>50):
				return False
	
	
	
		return True
		
	def read(self):
		GPIO.setmode(GPIO.BCM)

		GPIO.output(self.trig_pin, True)
		time.sleep(0.00001)
    	
		GPIO.output(self.trig_pin, False)
    	
		while GPIO.input(self.echo_pin) == 0:
			a=0
		pulse_start = time.time()
		while GPIO.input(self.echo_pin) == 1:
			a=0
		pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 1000000/58
		
		return distance 

	def process(self):

		#PERFORM REQUIRED CALCULATIONS
		data = self.read()

		if(data>500):
			return True,data 

		else:
			return data,False
		

		
