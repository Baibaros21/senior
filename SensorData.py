import json

class SensorData:
    def __init__(self, bikeid=0, distance=0,accelGyro = 0, impact=False, start = "True", accelerometer=0, gyroscope=0):
        self._bikeid = bikeid
        self._distance = distance
        self._accelerometer = accelerometer
        self._gyroscope = gyroscope
        self._impact = impact
        self._accelGyro = accelGyro
        self._start = start; 

    def to_string(self):
        data = {
            "distance": self._distance,
            "accelGyro": self._accelGyro,
            "impact": self._impact,
            "start": self._start
        }
        return json.dumps(data)

	# bikeid getter and setter
    @property
    def bikeid(self):
        return self._bikeid 

    @bikeid.setter
    def bikeid(self, value):
        self._bikeid = value

    # Distance getter and setter
    @property
    def distance(self):
        return self._distance 

    @distance.setter
    def distance(self, value):
        self._distance = value 
    
    #accelGyro getter and setter
    @property
    def accelGyro(self):
        return self._accelGyro 

    @distance.setter
    def accelGyro(self, value):
        self._accelGyro = value

    # Accelerometer getter and setter
    @property
    def accelerometer(self):
        return self._accelerometer

    @accelerometer.setter
    def accelerometer(self, value):
        self._accelerometer = value

    # Gyroscope getter and setter
    @property
    def gyroscope(self):
        return self._gyroscope

    @gyroscope.setter
    def gyroscope(self, value):
        self._gyroscope = value

    # Impact getter and setter
    @property
    def impact(self):
        return self._impact

    @impact.setter
    def impact(self, value):
        self._impact = value
    
    # start getter and setter
    @property
    def start(self):
        return self._start

    @impact.setter
    def start(self, value):
        self._start = value
