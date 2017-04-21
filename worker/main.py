# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-12 01:13 +0800
#
# Description: 
#


from gevent import monkey; monkey.patch_all()

import gevent.pywsgi
import signal
import application


import logging  
import logging.handlers  
  
def initLogger():
    logger = logging.getLogger()

    # fmt = logging.Formatter("%(asctime)s - %(pathname)s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")  
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s [%(filename)s,line%(lineno)s,%(funcName)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    fileHandler = logging.handlers.TimedRotatingFileHandler("../log/worker", 'H', 1, 0)
    fileHandler.suffix = "%Y%m%d-%H:%M.log"
    fileHandler.setFormatter(fmt)
    logger.addHandler(fileHandler)
    
    #cnslHandler = logging.StreamHandler()
    #cnslHandler.setFormatter(fmt)
    #logger.addHandler(cnslHandler)

    logger.setLevel(logging.DEBUG)
    logger.debug("logger init")


server = gevent.pywsgi.WSGIServer(("0.0.0.0", 8001), application.app)
def startServer():
    global server
    def stop_server(*args, **kwargs):
        global server
        server.stop()
        global stopTimer
        stopTimer = True
    
    #kill
    signal.signal(signal.SIGINT, stop_server)  
    #ctrl^C
    signal.signal(signal.SIGTERM, stop_server)
    #
    signal.signal(signal.SIGQUIT, stop_server)
    
    logger = logging.getLogger()
    logger.info("server started")
    #timer = gevent.spawn(incTimer)
    server.serve_forever()
    
    #gevent.joinall([timer])


if __name__ == "__main__":
    initLogger()
    startServer()
