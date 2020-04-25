import websockets
import asyncio
import json

async def hello(websocket, path):
    raw_data = await websocket.recv()
    data = json.loads(raw_data)

    print(f"got data {data}")

    if data.get("action") == "join":
        print("responding to join")
        await websocket.send(json.dumps({"name": "foo"}))

def start_websocket_server():
    server = websockets.serve(hello, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
