import tornado.ioloop

import time

import base.Server as svr
import base.MessageWorker as mw

import threading


def start():
    server = None
    try:
        server = svr.Server.get_instance()
        server.start_server()

        message_worker = mw.MessageWorker.get_instance()

        server.set_message_worker(message_worker)
        message_worker.set_server(server)

    except KeyboardInterrupt:
        if server is not None:
            server.stop_server()


if __name__ == "__main__":
    start()