import smbus
import math
import time
from Sensor import Sensor

class AccelGyroSensor(Sensor):
	def __init__(self, connections,location=None):
		self.name="Accelerometer & Gyroscope Sensor"
		self.bus = smbus.SMBus(connections[0]) #busNum
		self.address = connections[1] #address
        #power management registers
		self.power_mgmt_1 = connections[2]
		self.power_mgmt_2 = connections[3]
		if (location!=None):
			self.location=location
		else:
			location="middle"
        
	def register(self):
		try:
			self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
		except:
			return False
		return True
        
	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address, adr)
    
	def read_word(self, adr):
		high = self.bus.read_byte_data(self.address, adr)
		low = self.bus.read_byte_data(self.address, adr+1)
		val = (high << 8) + low
		return val
    
	def read_word_2c(self, adr):
		val = self.read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
 			return val
    
	def dist(self, a,b):
		return math.sqrt((a*a)+(b*b))
    
	def get_y_rotation(self, x,y,z):
		radians = math.atan2(x, self.dist(y,z))
		return -math.degrees(radians)
    
	def get_x_rotation(self, x,y,z):
		radians = math.atan2(y, self.dist(x,z))
		return math.degrees(radians)
    
	def get_z_rotation(self, x,y,z):
		radians = math.atan2(z, self.dist(x,y))
		return math.degrees(radians)
    
	def read(self):
		gyro_xout = self.read_word_2c(0x43)
		gyro_yout = self.read_word_2c(0x45)
		gyro_zout = self.read_word_2c(0x47)

		accel_xout = self.read_word_2c(0x3b)
		accel_yout = self.read_word_2c(0x3d)
		accel_zout = self.read_word_2c(0x3f)

		accel_xout_scaled = accel_xout / 16384.0
		accel_yout_scaled = accel_yout / 16384.0
		accel_zout_scaled = accel_zout / 16384.0
        
		x_rotation = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		y_rotation = self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		z_rotation = self.get_z_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        
		data = {
            "gyro_x": gyro_xout / 131,
            "gyro_y": gyro_yout / 131,
            "gyro_z": gyro_zout / 131,
            "accel_x": accel_xout_scaled,
            "accel_y": accel_yout_scaled,
            "accel_z": accel_zout_scaled,
            "x_rotation": self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled),
            "y_rotation": self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled),
            "z_rotation": self.get_z_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        		}

		return data
	def process(self):
		data  =self.read()
		warning  = False  
		return data,warning