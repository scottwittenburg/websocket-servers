import os
import uuid

import aiohttp
from aiohttp import web


STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dist')


async def init_app():
    app = web.Application()

    # https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-data-sharing
    app['clients'] = {}

    app.on_shutdown.append(shutdown)

    app.add_routes([web.static('/static', STATIC_FILES_PATH)])
    app.add_routes([web.get('/ws', echo_websocket_handler)])

    return app


async def shutdown(app):
    for client_data in app['clients'].values():
        ws = client_data['ws']
        await ws.close()
    app['clients'].clear()


async def echo_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    my_id = '{0}'.format(uuid.uuid4())
    request.app['clients'][my_id] = {
        'ws': ws
    }
    ws.set_cookie('mycustomsessionid', my_id)

    print("WebSocket opened ({0})".format(my_id))

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            elif msg.data.startswith('addgetter'):
                async def _getter(request):
                    return {'data': 1}
                request.app.router.add_get('/custom', _getter)
            else:
                await ws.send_str(u"You said: " + msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('WebSocket closed ({0})')

    return ws


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, port=8080)
