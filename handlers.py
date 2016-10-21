import asyncio

import websockets

from abstractions import BaseHandler


class ChatHandler(BaseHandler):
    client_pool = {}

    async def on_connected(self):
        print("Connected from {}".format(self._websocket.remote_address))
        self.client_pool[self._websocket.remote_address] = self._websocket

    async def on_disconnected(self):
        print("Disconnected from {}".format(self._websocket.remote_address))
        self.client_pool.pop(self._websocket.remote_address)

    async def on_receive(self, message):
        await asyncio.wait(
            [c.send(message) for c in self.client_pool.values()])

    async def send_to_client(self, client, message):
        try:
            await client.send(message)
        except websockets.ConnectionClosed:
            print("Connections closed during sending")
            self.client_pool.pop(client.remote_address)


class VideoHandler(BaseHandler):
    client_pool = {}

    async def on_connected(self):
        print("Connected from {}".format(self._websocket.remote_address))
        self.client_pool[self._websocket.remote_address] = self._websocket

    async def on_disconnected(self):
        print("Disconnected from {}".format(self._websocket.remote_address))
        self.client_pool.pop(self._websocket.remote_address)

    async def on_receive(self, message):
        await asyncio.wait(
            [c.send(message) for c in self.client_pool.values() if
             c != self._websocket])

    async def send_to_client(self, client, message):
        try:
            await client.send(message)
        except websockets.ConnectionClosed:
            print("Connections closed during sending")
            self.client_pool.pop(client.remote_address)
