import json
import SensorData 

class Trip:
    def __init__(self,bike_id):
        self.data = [] # contains all the data recorded during the trip
        self.warnings = [] # contains all the warnings identified during the trip
        self.warningData = []# contains 40 the data taken before a warning is detected during the trip
        self.bike_id = bike_id
    
    def add_data(self, sensorData):
        self.data.append(sensorData)


    # it add the list of the parametrs and the warning for each if existed
    def add_warning(self, json_obj):
         self.warnings.append(json_obj)
         self.warningData.append( self.get_data_warning(len(self.data)-1) )

    # it gets the previouse 40 readings when a wanring is detected
    def get_data_warning(self, index):
        if index < 40:
            return self.data[:index]
        else:
            return self.data[index-40:index]
