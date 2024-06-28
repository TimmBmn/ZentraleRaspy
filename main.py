import paho.mqtt.client as mqtt
import time

client = mqtt.Client("Zentrale")
# the broker should run on the same ip as the server no?
client.connect("192.168.135.191")
client.loop_start()


client.subscribe("sensorclient/data")

def on_message(client: mqtt.Client, userdata, msg):
    data = msg.payload.decode()

client.on_message = on_message

while True:
    time.sleep(1)
