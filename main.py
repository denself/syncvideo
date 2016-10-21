#!/usr/bin/env python

import asyncio
import logging

import websockets

from handlers import ChatHandler, VideoHandler

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

routes = [
    ('/chat', ChatHandler),
    ('/video', VideoHandler),
]


class Router(object):
    async def handle(self, websocket, path):
        for route, handler in routes:
            if route == path:
                obj = handler(websocket)
                await obj.on_connected()
                await obj.handle()
                await obj.on_disconnected()
                return


router = Router()
start_server = websockets.serve(router.handle, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
