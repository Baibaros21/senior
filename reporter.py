import PubSub 
import json
import requests
import trip 
import SensorData

class Reporter():
    #In this class we will have a trip object which contains all data, warnings, and the data requried for each warning 
    #check warning class for further details about
    def __init__(self,bike_id):
        self.pubsub = PubSub.MQTTPubSub()
        self.bike_id = bike_id 
        self.trip = trip.Trip(bike_id)
        #This array will contains links for the API required for sensor failiure reporting and data uploading 
        self.links = ['https://0os1xxpsq4.execute-api.us-east-1.amazonaws.com/testing/invokedynamo']
    #waits until the driver start the trip
    def waitForTripStart(self):
        self.pubsub.subscribe(self.bike_id)
        while(self.pubsub.start==False):
            pass
        return True

    #return true if the trip is stop either by driver or ISR of FSR
    def isTripDone(self):
        if(self.pubsub.start==False):
            print("Driver Ended the Trip\n Disconnecting.....")
            self.pubsub.disconnect()
            return True
        else:
            return False


   #API calls. To be updated
    def uploadtripData(self):
        self._invokeApi(self.trip.warningData,self.links[0])

    def reportSensorFault(self, data):
        self._invokeApi(data,self.links[0])

    #This process function collects the data from process function of eahc sensor
    #It check if there is any warnong from any sensors, if true it warns the driver
    def porcess(self, ultrasonic,accelGyro,impact):
        sensorData = SensorData.SensorData(self.bike_id) 

        sensorData.distance = ultrasonic["data"]
        sensorData.accelGyro = accelGyro["data"]
        sensorData.impact = impact["data"] 
        #adding the collected data
        self.trip.add_data(sensorData)

        if(ultrasonic["warning"] or accelGyro["warning"] or impact["warning"]):
            warningData  = {
                "distance": ultrasonic["warning"],
                "accelGyro": accelGyro["warning"],
                "impact": impact["warning"]}
            #warn the driver and save the required data collected for uploading
            self._warnDriver(json.dumps(warningData))
            self.trip.add_warning(warningData)    

    def reprotImpact(self,location):
        data = {"accident": location}
        self._warnDriver(json.dumps(data))
        self.pubsub.start=False
    
    
    def _warnDriver(self,data):
        self.pubsub.publish(self.bike_id,data)

    def _invokeApi(data,link):
        a=0
        # Set the endpoint URL and payload
        url = link
        payload = data

        # Set the headers
        headers = {'Content-Type': 'application/json'}

        # Convert the payload to a JSON string
        json_payload = json.dumps(payload)

        # Make the POST request
        response = requests.post(url, headers=headers, data=json_payload)

        # Print the response
        print(response.content)   


