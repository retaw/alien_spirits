# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-11 04:16 +0800
#
# Description: 
#

from flask import Flask
from flask import request

timer_counter = 0


app = Flask(__name__)
app.debug = True

@app.route("/")
def action_default():
    return "Hello, World"

#/test?name=hahah&age=123
@app.route("/test2", methods=["GET", "POST"])
def action_test2():
    if request.method == "GET":
        name = request.args.get("name")
        age  = request.args.get("age")
    elif request.method == "POST":
        name = request.form.get("name")
        age  = request.form.get("age")
    return "method: {}, name: {}, age: {}\n".format(request.method, name, age)
    return "method: {}, request: {}\ndata: {}\nget_data: {}\n".format(request.method, request, str(request.data), str(request.get_data()))


@app.route("/test1/")
def action_test1():
    return "test1"

@app.route("/hello/<somebody>/name")
def action_hello(somebody):
    return "msg:{}".format(somebody)


