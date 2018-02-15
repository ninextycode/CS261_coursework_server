import tornado.ioloop

import time

import base.Server as svr


ioloop = tornado.ioloop.IOLoop.instance()

try:
    svr.start_server()

    while True:
        ioloop.add_callback(lambda :svr.Server.send_message("ALERT"))
        time.sleep(5)

except KeyboardInterrupt:
    ioloop.add_callback(ioloop.stop)