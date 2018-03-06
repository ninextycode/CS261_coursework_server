import tornado.ioloop

import time

import base.server as svr
import base.message_worker as mw
import business_logic.message_routing.message_router as mr

import threading
import signal


def start():
    server: svr.Server = None
    # todo send special message on server restart
    server = svr.Server.get_instance()
    message_worker = mw.MessageWorker.get_instance()
    message_router = mr.MessageRouter.get_instance()

    server.start_server()

    server.set_message_worker(message_worker)
    message_worker.set_server(server)

    message_worker.set_message_router(message_router)
    message_router.set_message_worker(message_worker)
    signal.signal(signal.SIGINT, server.stop_server)



if __name__ == '__main__':
    start()