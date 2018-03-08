import tornado.ioloop

import time

import base.server as svr
import base.message_worker as mw
import business_logic.message_routing.message_router as mr
import business_logic.notifications.subscription_checker as s_ch


import threading
import signal
import business_logic.data_processing.stock_database_updater as stock_database_updater


def start():
    # todo send special message on server restart
    server = svr.Server.get_instance()
    message_worker = mw.MessageWorker.get_instance()
    message_router = mr.MessageRouter.get_instance()

    server.start_server()

    server.set_message_worker(message_worker)
    message_worker.set_server(server)

    message_worker.set_message_router(message_router)
    message_router.set_message_worker(message_worker)

    checker: s_ch.SubscriptionChecker = s_ch.SubscriptionChecker.get_instance()
    checker.start()

    updater: stock_database_updater.StockDatabaseUpdater = stock_database_updater.StockDatabaseUpdater.get_instance()
    updater.start()
    signal.signal(signal.SIGINT, server.stop_server)



if __name__ == '__main__':
    start()