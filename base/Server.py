import tornado.websocket as tws
import tornado.web as tw
import tornado.httpserver as t_http
import tornado.ioloop

import threading
import json

import base.Log as l
import config


class Handler(tws.WebSocketHandler):
    on_message_callback = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with Server.main_lock:
            Server.get_instance().live_handlers.add(self)

    def open(self):
        pass

    def on_message(self, message):
        Handler.on_message_callback(message)
        l.log("Server received {}".format(message))

    def on_close(self):
        l.log(self, "disconnected")
        with Server.main_lock:
            handlers = Server.get_instance().live_handlers
            if self in handlers:
                handlers.remove(self)


class Server:
    instance = None
    main_lock = threading.Lock()

    @staticmethod
    def get_instance():
        if Server.instance is None:
            with Server.main_lock:
                if Server.instance is None:
                    Server.instance = Server()
        return Server.instance

    def __init__(self):
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
        with Server.main_lock:
            for m in self.messages_to_send:
                self.unsafe_send(m)
            self.messages_to_send = []

    def unsafe_send(self, message):
        self.unsafe_clean_live_handlers_list()
        if len(self.live_handlers) > 0:
            l.log("Server sends {}".format(message))
        else:
            l.log("No active connections to send {}".format(message))

        for ws in self.live_handlers:
            ws.write_message(message)

    def on_message(self, message):
        with Server.main_lock:
            self.unsafe_on_message(message)

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