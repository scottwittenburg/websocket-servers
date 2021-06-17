import asyncio
import os
import time
import uuid

import aiohttp
from aiohttp import web
from aiohttp.web import middleware


STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dist')


# @middleware
# async def create_session(request, handler):
#     print('create_session, path: {0}'.format(request.path))
#     response = await handler(request)
#     session_id = request.cookies.get('my_custom_session_id')
#     if not session_id:
#         session_id = '{0}'.format(uuid.uuid4())
#         print('CREATE ONCE, session_id: {0}'.format(session_id))
#         response.headers['Set-Cookie'] = 'my_custom_session_id={}'.format(session_id)
#         request.app['clients'][session_id] = {
#             'id': session_id,
#         }
#     else:
#         print('FOUND session_id: {0}'.format(session_id))

#     return response


# async def on_prepare(request, response):
#     print('on_prepare, path: {0}'.format(request.path))
#     session_id = request.cookies.get('my_custom_session_id')
#     if not session_id:
#         session_id = '{0}'.format(uuid.uuid4())
#         print('CREATE ONCE, session_id: {0}'.format(session_id))
#         response.headers['Set-Cookie'] = 'my_custom_session_id={}'.format(session_id)
#         request.app['clients'][session_id] = {
#             'id': session_id,
#         }
#     else:
#         print('FOUND session_id: {0}'.format(session_id))

#     return response


async def shutdown(app):
    print('Closing client websockets')
    for client_data in app['clients'].values():
        print('  {0}'.format(client_data['id']))
        ws = client_data['ws']
        await ws.close()
    app['clients'].clear()


async def echo_websocket_handler(request):
    print('enter echo_websocket_handler')

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # session_id = request.cookies.get('my_custom_session_id')
    # if session_id:
    #     session_id = request.cookies['my_custom_session_id']
    #     print('I already know this person: {0}'.format(session_id))
    #     client_info = request.app['clients']
    #     if session_id not in client_info:
    #         print('but I do not have client_info for them')
    #         client_info[session_id] = {}
    #     client_info[session_id]['ws'] = ws
    # else:
    #     print('No session id')

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

    # print('WebSocket closed ({0})'.format(session_id))
    print('WebSocket closed')

    return ws


async def long_running_task(request):
    # You can't just sleep, you have to do it asynchronously
    #time.sleep(15)
    await asyncio.sleep(15)
    return web.Response(text="That was a nice nap!")


async def init_app():
    # app = web.Application(middlewares=[create_session])

    app = web.Application()
    # app.on_response_prepare.append(on_prepare)

    # https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-data-sharing
    app['clients'] = {}

    app.on_shutdown.append(shutdown)

    app.add_routes([web.static('/static', STATIC_FILES_PATH)])
    app.add_routes([web.get('/ws', echo_websocket_handler)])
    app.add_routes([web.get('/slow', long_running_task)])

    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, port=8080)
