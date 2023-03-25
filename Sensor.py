from abc import ABC, abstractmethod


class Sensor(ABC):
	

	
	@abstractmethod
	def __init__(self, connections,location):
		pass
	
	@abstractmethod
	def register(self):
		pass
	
	@abstractmethod
	def read(self):
		pass
	@abstractmethod
	def process(self):
		pass
	def error(self):
		return self.name + " at the "+ self.location + " is not working"
	
		
	
	
