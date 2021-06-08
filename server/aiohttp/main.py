import os

import aiohttp
from aiohttp import web


STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dist')


async def echo_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("WebSocket opened")

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(u"You said: " + msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('WebSocket closed')

    return ws


app = web.Application()
app.add_routes([web.static('/static', STATIC_FILES_PATH)])
app.add_routes([web.get('/ws', echo_websocket_handler)])


if __name__ == '__main__':
    web.run_app(app, port=8080)
