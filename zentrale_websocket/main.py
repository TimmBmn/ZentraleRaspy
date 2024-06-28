import paho.mqtt.client as mqtt
import websockets
import time


def start_websocket():
    client = mqtt.Client("Timms Zentrale")
    client.connect("172.19.72.246")
    client.loop_start()
    client.subscribe("sensorclient/data")

    def on_message(client: mqtt.Client, userdata, msg):
        data = msg.payload.decode()
        print(data)

    client.on_message = on_message

    while True:
        time.sleep(1)


if __name__ == '__main__':
    start_websocket()
