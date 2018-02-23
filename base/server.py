import tornado.websocket as tws
import tornado.web as tw
import tornado.httpserver as t_http
import tornado.ioloop

import threading
import json
import traceback

import base.log as l
import base.singleton as sn
import config


handler_logger = l.Logger("Handler")


class Handler(tws.WebSocketHandler):
    on_message_callback = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        handler_logger.log(self, "connected")
        Server.get_instance().add_handler(self)

    def open(self):
        pass

    def on_message(self, message):
        handler_logger.log(" received {}".format(message))
        Handler.on_message_callback(message)

    def on_close(self):
        handler_logger.log(self, "disconnected")
        Server.get_instance().remove_handler(self)


server_logger = l.Logger("Server")


class Server(sn.Singleton):
    def __init__(self):
        self.handlers_lock = threading.Lock()
        self.sending_message_lock = threading.Lock()
        self.receiving_message_lock = threading.Lock()

        self.message_worker = None
        self.live_handlers = set()
        self.messages_to_send = []

        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ioloop_thread = None
        Handler.on_message_callback = self.on_message

    def set_message_worker(self, worker):
        self.message_worker = worker

    def unsafe_clean_live_handlers_list(self):
        to_remove = set()
        for ws in self.live_handlers:
            if not (ws.ws_connection and ws.ws_connection.stream and ws.ws_connection.stream.socket):
                to_remove.add(ws)

        self.live_handlers = self.live_handlers - to_remove

    def send(self, message):
        self.send_in_future(message)

    def send_in_future(self, message):
        self.messages_to_send.append(message)

    def send_queued(self):
        with self.sending_message_lock:
            for m in self.messages_to_send:
                self.unsafe_send(m)
            self.messages_to_send = []

    def unsafe_send(self, message):
        self.unsafe_clean_live_handlers_list()
        if len(self.live_handlers) > 0:
            server_logger.log("Server sends {}".format(message))
        else:
            server_logger.log("No active connections to send {}".format(message))

        for ws in self.live_handlers:
            ws.write_message(message)

    def on_message(self, message):
        with self.receiving_message_lock:
            response = {
                "type": "message",
                "data": {
                    "mime_type": "text/plain",
                    "body": "test response"
                }
            }
            try:
                self.unsafe_on_message(message)
            except Exception as e:
                response["data"]["body"] = traceback.format_exc()
                response["type"] = "exception"

            self.send(response)

    def unsafe_on_message(self, message):
        message_json = json.loads(message)
        self.message_worker.on_message(message_json)

    def start_server(self):
        application = tw.Application([
            (r'/', Handler),
        ])

        http_server = t_http.HTTPServer(application)
        http_server.listen(config.ws_port)
        message_send_period_ms = 100

        send_messages = tornado.ioloop.PeriodicCallback(self.send_queued, message_send_period_ms)

        def start_in_thread():
            send_messages.start()
            self.ioloop.start()

        self.ioloop_thread = threading.Thread(target=start_in_thread)
        self.ioloop_thread.start()

    def stop_server(self):
        self.ioloop.add_callback(self.ioloop.stop)

    def add_handler(self, h):
        with self.handlers_lock:
            self.live_handlers.add(h)

    def remove_handler(self, h):
        with self.handlers_lock:
            self.live_handlers.remove(h)