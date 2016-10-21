import websockets


class BaseHandler(object):
    def __init__(self, websocket):
        """
        :param websocket: connection to WebSocket
        :type websocket: websockets.WebSocketServerProtocol
        """
        self._websocket = websocket

    async def on_connected(self):
        pass

    async def on_disconnected(self):
        pass

    async def on_receive(self, message):
        pass

    async def handle(self):
        while True:
            try:
                message = await self._websocket.recv()
            except websockets.ConnectionClosed:
                break
            else:
                await self.on_receive(message)

    async def send(self, message):
        self._websocket.send(message)