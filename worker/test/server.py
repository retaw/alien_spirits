# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-10 17:45 +0800
#
# Description: 
#


from gevent import monkey; monkey.patch_all()

import gevent.pywsgi
import signal


def app(environ, start_response):
    print environ, "\n"
    response_headers = [('Content-Type', 'text/plain')]
    start_response("200 OK", response_headers)
    return ["abc", "ddf", "13457", "\n"]

server = gevent.pywsgi.WSGIServer(("0.0.0.0", 8000), app)

def stop_server(*args, **kwargs):
    server.stop()

signal.signal(signal.SIGINT, stop_server)
signal.signal(signal.SIGQUIT, stop_server)

server.serve_forever()


