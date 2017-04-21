# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-10 17:45 +0800
#
# Description: 
#


from gevent import monkey; monkey.patch_all()

import gevent.wsgi
import signal

def application(environ, start_respones):
    print environ
    status = "200 ok"
    response_headers = [("Content-Type", "text/plain")]
    start_respones(status, response_headers)
    return ["welcome to gevent lesson"]

server = gevent.pywsgi.WSGIServer(("0.0.0.0", 8000), application)

def stop_server(*args, **kwargs):
    server.stop()

signal.signal(signal.SIGINT, stop_server)

server.serve_forever()


