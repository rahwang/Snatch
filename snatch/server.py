import websockets
import asyncio
import json
from random import choice


# eventually we will have to do somethign like this: https://websockets.readthedocs.io/en/stable/intro.html#both
# probably use a queue a la this to push state to clients when things chage: https://stackoverflow.com/questions/51548025/asyncio-multithreaded-server-with-two-coroutines

POSSIBLE_NAMES = ["jamie", "rachel", "james", "someone else"]

class Server():

    def __init__(self):
        self.game = {}
        self.updates = asyncio.Queue()
        self.clients = {}

    async def handle(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.request_handler(websocket, path))
        producer_task = asyncio.ensure_future(self.update_handler(websocket, path))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    async def request_handler(self, websocket, path):
        async for raw_data in websocket:
            data = json.loads(raw_data)
            print(f"got data {data}")
            await self.handle_request(data, websocket)

    async def handle_request(self, data, websocket):
        print("in handle request")
        if data.get("action") == "join":
            name = choice(POSSIBLE_NAMES)  ## TODO exclude already chosen names
            self.clients[name] = websocket
            self.game[name] = 0
        await self.update_clients()

    async def update_clients(self):
        print("putting update on queue")
        await self.updates.put(self.game)

    async def update_handler(self, websocket, path):
        while True:
            print("in update")
            new_game_state = await self.updates.get()
            print("got update off queue")
            message = json.dumps(new_game_state)
            for client in self.clients.values():
                await client.send(message)

def start_websocket_server():
    server = Server()
    socker_server = websockets.serve(server.handle, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(socker_server)
    asyncio.get_event_loop().run_forever()
