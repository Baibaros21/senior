from Sensor import Sensor
import RPi.GPIO as GPIO
import time

class FSR(Sensor):
	def __init__(self, connections, location, reporter):
		self.name="Impact Sensor"
		self.fsr_pin=connections[0]
		self.location=location
		self.reporter=reporter

	def register(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.fsr_pin, GPIO.IN)
		print("FSR at location ",self.location," registered sucessfuly")
		
		
	def action(self):
		self.impactDetected=True
		self.reporter.reportImpact(self.location)
		print("Impact detcetd from FSR at location ",self.location)

	def read(self):
		print("Setting event to detected impact from FSR at location ",self.location)
		GPIO.setmode(GPIO.BCM)
		GPIO.add_event_detect(self.fsr_pin,GPIO.RISING, self.action, bouncetime=1000)
	
	def process(self):
		return self.impactDetected