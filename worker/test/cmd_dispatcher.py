# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-11 00:21 +0800
#
# Description: 
#

def application(environ, start_respones):
    print environ
    status = "200 ok"
    response_headers = [("Content-Type", "text/plain")]
    start_respones(status, response_headers)
    return ["unvaliable request"]


class Dispatcher:
    __methodActionMap = {}

    def __init__(self):
        __methodActionMap.update(
        return

    def dispatch(method, **args):
        
