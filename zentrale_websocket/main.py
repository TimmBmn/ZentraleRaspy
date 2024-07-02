from __future__ import annotations
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import websockets.server
import websockets
import asyncio
import json
import os


class Connections:
    clients: list[websockets.server.WebSocketServerProtocol] = []


async def handler(websocket: websockets.server.WebSocketServerProtocol):
    async for message in websocket:
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            await websocket.send(json.dumps({"status": "error", "message": "message wasn't a json object"}))
            continue

        if not isinstance(data, dict):
            await websocket.send(json.dumps({"status": "error", "message": "message wasn't a json object"}))
            continue

        try:
            data["type"]
        except KeyError:
            await websocket.send(json.dumps({"status": "error", "message": "type is missing"}))
            continue

        if data["type"] == "connect":
            Connections.clients.append(websocket)
            await websocket.send("Hi")


async def main():
    await websockets.serve(handler, "127.0.0.1", 8765)
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

    # filter out disconnected clients
    Connections.clients = [websocket for websocket in Connections.clients if websocket.state == 1] 
    websockets.broadcast(Connections.clients, json.dumps(data))
    print("broadcast")


def start_websocket():
    load_dotenv()
    broker_ip = os.getenv("BROKER_IP")
    if broker_ip is None:
        raise Exception("no broker ip in .env")


    client = mqtt.Client("Timms Zentrale")
    client.connect(broker_ip)
    client.loop_start()
    client.subscribe("sensorclient/data")
    client.on_message = on_message

    asyncio.run(main())


if __name__ == '__main__':
    start_websocket()
