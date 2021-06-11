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
    app.add_routes([web.get('/custom', registration_handler)])

    return app


async def on_prepare(request, response):
    if 'mycustomsessionid' not in request.cookies:
        my_id = '{0}'.format(uuid.uuid4())

        request.app['clients'][my_id] = {
            'id': my_id,
        }

        response.set_cookie('mycustomsessionid', my_id)

    response.headers['My-Header'] = 'value'


async def registration_handler(request):
    response = web.Response(text="Hello, world")

    my_id = '{0}'.format(uuid.uuid4())

    request.app['clients'][my_id] = {
        'id': my_id,
    }

    response.set_cookie('mycustomsessionid', my_id)

    return response


async def shutdown(app):
    for client_data in app['clients'].values():
        ws = client_data['ws']
        await ws.close()
    app['clients'].clear()


async def echo_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    my_id = None

    if 'mycustomsessionid' in request.cookies:
        my_id = request.cookies['mycustomsessionid']
        request.app['clients'][my_id]['ws'] = ws
    else:
        print('No session id')

    # my_id = '{0}'.format(uuid.uuid4())
    # request.app['clients'][my_id] = {
    #     'ws': ws
    # }

    # Not sure if this is actually working just by looking at the network
    # tab in the web console.
    #
    # ws.set_cookie('mycustomsessionid', my_id)
    #
    # Related issue:
    #
    #     https://github.com/aio-libs/aiohttp/issues/2053

    # print("WebSocket opened ({0})".format(my_id))
    print("WebSocket opened")

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            # Attempting to add dynamic route this way results in:
            #
            #     RuntimeError: Cannot register a resource into frozen router.
            #
            # Alternatives are to register a route that handles all possible
            # paths, then do custom routing, or to write a custom dispatcher:
            #
            #     https://github.com/aio-libs/aiohttp/issues/1540
            #
            # elif msg.data.startswith('addgetter'):
            #     async def _getter(request):
            #         return {'data': 1}
            #     request.app.router.add_get('/custom', _getter)
            else:
                await ws.send_str(u"You said: " + msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    # print('WebSocket closed ({0})'.format(my_id))
    print('WebSocket closed')

    return ws


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, port=8080)
