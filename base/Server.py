import tornado.websocket as tws
import tornado.web as tw
import tornado.httpserver as t_http
import tornado.ioloop

import threading

import base.Log as l
import config


class Server(tws.WebSocketHandler):
    live_websockets = set()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Server.live_websockets.add(self)

    def open(self):
        pass

    def on_message(self, message):
        l.log("Server received {}".format(message))

    @staticmethod
    def send_message(message):
        Server.clean_sockets_list()
        if len(Server.live_websockets) > 0:
            print("Server sends {}".format(message))
        else:
            print("No active connections to send {}".format(message))

        for ws in Server.live_websockets:
            ws.write_message(message)

    @staticmethod
    def clean_sockets_list():
        to_remove = set()
        for ws in Server.live_websockets:
            if not (ws.ws_connection and ws.ws_connection.stream.socket):
                to_remove.add(ws)

        Server.live_websockets = Server.live_websockets - to_remove

    def on_close(self):
        l.log(self, "disconnected")
        Server.live_websockets.remove(self)


def start_server():
    application = tw.Application([
        (r'/', Server),
    ])

    http_server = t_http.HTTPServer(application)
    http_server.listen(config.ws_port)

    def start_loop():
        loop = tornado.ioloop.IOLoop.instance()
        loop.start()

    thread = threading.Thread(target=start_loop)
    thread.start()

