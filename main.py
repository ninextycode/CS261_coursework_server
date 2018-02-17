import tornado.ioloop

import time

import base.Server as svr
import base.MessageWorker as mw

import threading


def start():
    try:
        server = svr.Server.get_instance()
        message_worker = mw.MessageWorker.get_instance()

        server.message_worker = message_worker
        message_worker.server = server

    except Exception:
        return

    try:
        server.start_server()
        while True:
            ts = [threading.Thread(
                    target=lambda : server.send_in_future({"body":threading.get_ident() % 41}))
                    for i in range(10)]

            [t.start() for t in ts]
            [t.join() for t in ts]
            server.send_in_future({"body": "ALERT"} )
            time.sleep(2)

    except KeyboardInterrupt:
        server.stop_server()

start()