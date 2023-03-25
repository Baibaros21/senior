import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import json 
import threading 

class MQTTPubSub:

    # Connect to AWS IoT Core
    def connect(self):
        global client
        client.connect()

    # Publish a message to a topic
    def publish(slef,topic,message):
        global client
        client.publish(topic, message, 1)
        print(f'Published message on topic {topic}: {message}')

    # Subscribe to a topic
    def custom_callback(self, client, userdata, message):
        msg = json.loads(message.payload)
        print(f'Received message on topic {message.topic}: {msg}')
        if(msg['start']=="True"):
            self.start=True
        else:
            self.start=False

    def subscribe(self, topic):
        global client
        client.subscribe(topic, 1, self.custom_callback)

    # Disconnect from AWS IoT Core
    def disconnect(self):
        global client
        client.disconnect()
        
    def __init__(self) -> None:
        global client
        # Setup AWS credentials
        aws_access_key_id = 'AKIAT3I7RJXEK5G4P2HN'
        aws_secret_access_key = '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'
        aws_region = 'ap-northeast-1'
        endpoint = "acwia3i5iqvrr-ats.iot.ap-northeast-1.amazonaws.com"
        client_id = "gehanAbdelelatif"

        # Define paths to your AWS IoT Core credentials (replace with your own paths)
        ca_cert = "./certs/AmazonRootCA1.pem"
        cert = "./certs/certificate.pem.crt" 
        key = "./certs/private.pem.key"



        # Initialize AWS IoT client
        iot_client = boto3.client('iot', aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=aws_region)

        iot_endpoint = iot_client.describe_endpoint(endpointType='iot:Data-ATS')['endpointAddress']

        client = AWSIoTMQTTClient(client_id)
        client.configureConnectDisconnectTimeout(10)  # set the connect and disconnect timeout to 10 seconds
        client.configureMQTTOperationTimeout(5)  # set the MQTT operation timeout to 5 seconds
        client.configureOfflinePublishQueueing(-1)  # set the queue size to -1 to disable queueing
        client.configureDrainingFrequency(2)  # set the draining frequency to 2 Hz

        client.configureEndpoint(endpoint, 8883)
        client.configureCredentials(ca_cert , key , cert)
        
        self.start = False
        self.connect()
