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
from flask_cors import CORS

import json
from userManager import UserManager


userManager = UserManager()

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route("/")
def action_default():
    return "Error, bad request"


# get_user_id
@app.route("/get_user_id", methods=["GET", "POST"])
#@crossdomain(origin='*')
def action_get_user_id():
    if request.method == "GET":
        openId = request.args.get("openid")
    else:
        return redirect(url_for("/"))

    def checkOpenId(openId):
        return True
        if len(openId) != 16:
            return False
        try:
            openIdValue = int(openId, 16)
            if openIdValue == 0:
                return False
        except:
            return False
        return True

    if not checkOpenId(openId):
        return "bad openid"

    userId, avaliablePower, reverseRefreshTimes = userManager.getUserBasicInfo(openId)
    ret = {"userid": userId, "reverse_refresh_times": reverseRefreshTimes, "avaliable_power": avaliablePower}
    print "get_user_id, ret:", ret
    return json.dumps(ret)

#get_items_on_map
@app.route("/get_items_on_map", methods=["GET", "POST"])
def action_get_items_on_map():
    if request.method == "GET":
        userId = request.args.get("userid")
    else:
        return redirect(url_for("/"))

    userId = int(userId)
    itemsOnMap = userManager.getUserItemsOnMap(userId)
    ret = {"items_on_map": itemsOnMap}
    return json.dumps(ret)

#refresh_items_on_map
@app.route("/refresh_items_on_map", methods=["GET", "POST"])
def action_refresh_items_on_map():
    if request.method == "GET":
        userId   = request.args.get("userid")
        coordlat = request.args.get("coordlat")
        coordlng = request.args.get("coordlng")
    else:
        return redirect(url_for("/"))

    print "coordlat:", coordlat
    print "coordlng:", coordlng

    userId = int(userId)
    lat = float(coordlat)
    lng = float(coordlng)

    retCode, reverseRefreshTimes, itemsOnMap = userManager.refreshUserItemsOnMap(userId, lat, lng)
    ret = {"op_ret": retCode, "reverse_refresh_times": reverseRefreshTimes, "items_on_map": itemsOnMap}
    return json.dumps(ret)

#force_refresh_items_on_map_today
@app.route("/force_refresh_items_on_map_today", methods=["GET", "POST"])
def force_refresh_items_on_map_today():
    if request.method == "GET":
        userId   = request.args.get("userid")
        coordlat = request.args.get("coordlat")
        coordlng = request.args.get("coordlng")
    else:
        return redirect(url_for("/"))

    print "coordlat:", coordlat
    print "coordlng:", coordlng

    userId = int(userId)
    lat = float(coordlat)
    lng = float(coordlng)

    retCode, reverseRefreshTimes, itemsOnMap = userManager.systemForceRefreshUserItemsOnMapToday(userId, lat, lng)
    ret = {"op_ret": retCode, "reverse_refresh_times": reverseRefreshTimes, "items_on_map": itemsOnMap}
    return json.dumps(ret)

#capture_item_on_map
@app.route("/capture_item_on_map", methods=["GET", "POST"])
def capture_item_on_map():
    if request.method == "GET":
        userId   = request.args.get("userid")
        itemIndex= request.args.get("item_index")
        coordlat = request.args.get("coordlat")
        coordlng = request.args.get("coordlng")
    else:
        return redirect(url_for("/"))

    userId    = int(userId)
    itemIndex = int(itemIndex)
    lat = float(coordlat)
    lng = float(coordlng)
    retCode = 0
    reverseRefreshTimes = 0
    itemsOnMap = []
    retCode, avaliablePower, itemsOnMap = userManager.captureItem(userId, itemIndex, lat, lng)
    ret = {"op_ret": retCode, "avaliable_power": avaliablePower, "items_on_map": itemsOnMap}
    return json.dumps(ret)


#get_items_captured
@app.route("/get_items_captured", methods=["GET", "POST"])
def action_get_items_captured():
    if request.method == "GET":
        userId   = request.args.get("userid")
    else:
        return redirect(url_for("/"))

    userId    = int(userId)
    itemsCaptured, uniqueCode = userManager.getUserItemsCaptured(userId)
    ret = {"unique_code": uniqueCode, "items": itemsCaptured}
    return json.dumps(ret)


#add_power
@app.route("/add_power", methods=["GET", "POST"])
def add_power():
    if request.method == "GET":
        userId      = request.args.get("userid")
        actType     = request.args.get("act_type")
        videoCode   = request.args.get("video_code")
    else:
        return redirect(url_for("/"))


    userId  = int(userId)
    actType = int(actType)
    if videoCode == None:
        videoCode = 0
    else:
        videoCode = int(videoCode)

    retCode, avaliablePower, extraPower = userManager.addPower(userId, actType, videoCode)
    ret = {"op_ret": retCode, "avaliable_power": avaliablePower, "extra_power": extraPower}
    return json.dumps(ret)


#/test?name=hahah&age=123
@app.route("/test2", methods=["GET", "POST"])
def action_test2():
    print request.environ, "\n"
    if request.method == "GET":
        name = request.args.get("name")
        age  = request.args.get("age")
    elif request.method == "POST":
        name = request.form.get("name")
        age  = request.form.get("age")
    return "method: {}, request: {}\nform: {}\nget_data: {}\n".format(request.method, request, str(request.form), str(request.stream.read()))



