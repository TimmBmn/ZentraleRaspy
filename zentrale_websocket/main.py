import paho.mqtt.client as mqtt
import websockets.server
import websockets
import asyncio
import json


class asdf:
    connections: dict = {}

    def __init__(self, websocket: websockets.server.WebSocketServerProtocol) -> None:
        self.websocket = websocket

    @property
    def connected(self):
        connected = self.websocket is not None and self.websocket.state > 1
        if not connected:
            del asdf.connections[self.websocket.id]


async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            websocket.send(json.dumps({"status": "error", "message": "message wasn't a json object"}))
            continue

        if not isinstance(data, dict):
            websocket.send(json.dumps({"status": "error", "message": "message wasn't a json object"}))
            continue

        try:
            data["type"]
        except KeyError:
            websocket.send(json.dumps({"status": "error", "message": "type is missing"}))
            continue

        if data["type"] == "connect":
            asdf.connections[websocket.id] = asdf(websocket)


async def main():
    await websockets.serve(handler, "localhost", 6000)
    await asyncio.Future() # run forever


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    if msg.topic != "sensorclient/data":
        print("can't handel that topic: " + msg.topic)
        return

    try:
        raw_data = json.loads(msg.payload.decode())
    except json.decoder.JSONDecodeError:
        print("data send in wrong format")
        return

    data = {
        "room": raw_data[0],
        "wet": raw_data[1],
        "temp": raw_data[2],
        "temp_limit": raw_data[3]
    }

    websockets.broadcast([connection for connection in asdf.connections if connection.connected], json.dumps(data))


def start_websocket():
    client = mqtt.Client("Timms Zentrale")
    client.connect("172.19.72.246")
    client.loop_start()
    client.subscribe("sensorclient/data")
    client.on_message = on_message

    asyncio.run(main())


if __name__ == '__main__':
    start_websocket()
