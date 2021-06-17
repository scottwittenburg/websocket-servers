import asyncio
import os
import time

import tornado.ioloop
import tornado.web
import tornado.websocket


STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dist')


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        if message == 'close':
            self.close()
        else:
            self.write_message(u"You said: " + message)

    def on_close(self):
        # Closing the client browser tab, e.g. closes the websocket
        print("WebSocket closed")


class LongRunningHandler(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(15)
        self.write("That was a nice nap!")


def make_app():
    # This page shows how to set up static file serving:
    #
    #     https://www.tornadoweb.org/en/stable/guide/running.html#static-files-and-aggressive-file-caching
    #
    # And here you can see the "static_url_prefix" setting lets you customize the default static path of "/static/":
    #
    #    https://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
    #
    settings = {
        "static_path": STATIC_FILES_PATH,
    }

    return tornado.web.Application([
        (r"/ws", EchoWebSocket),
        (r"/slow", LongRunningHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
