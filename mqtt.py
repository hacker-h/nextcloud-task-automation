import paho.mqtt.client as mqtt
import os

# Create a client instance
client = mqtt.Client()
broker_address = os.getenv("MQTT_HOSTNAME")
broker_port = int(os.getenv("MQTT_PORT"))

# set username and password for authentication
client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))

def initialize():
    # Connect to the broker
    client.connect(broker_address, broker_port)

def publish(message : str, topic : str):
    # Publish the message to the specified topic
    client.publish(topic, message)

initialize()

# # Disconnect from the broker
# client.disconnect()
