# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-14 15:26 +0800
#
# Description:  经纬度相关算法实现， 以下单位全部为 km
#

from math import sin, asin, cos, radians, fabs, sqrt, degrees


# 地球半径, 维基百科数据
EARTH_RADIUS=6376.5           


def hav(theta):
    s = sin(theta / 2.0)
    return s * s


#haversine公式, 计算地球表面两点间的最短距离（弧长）
def getDistHaverisine(lat0, lng0, lat1, lng1):
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance

#给定地球纬度坐标，该纬度对应的纬线圈上截取一定长度的弧线段，弧线段两端对应的经度坐标差
def getLongitudeShift(lat0, distance):
    lat = radians(lat0)
    #偏移(弧度) = 距离/纬线圈的周长
    dlng = distance / (EARTH_RADIUS * cos(lat))
    #弧度转角度
    ret = degrees(dlng)
    #溢出修正
    def adjustOverFlow(ret):
        if ret > 0:
            ret = ret % 360
        else:
            ret = ret % -360
        if ret > 180:
            ret = ret - 360
        elif ret < -180:
            ret = ret + 360
        return ret
    return adjustOverFlow(ret)


#经线圈上截取一定长度的弧线段，弧线段两段对应的纬度坐标差
def getLatitudeShift(distance):
    #偏移(弧度) = 距离/经线圈的周长
    dlat = distance / EARTH_RADIUS
    #弧度转角度
    ret = degrees(dlat)
    #溢出修正
    def adjustOverFlow(ret):
        if ret > 0:
            ret = ret % 360
        else:
            ret = ret % -360
        if ret > 180:
            ret = 180 - ret
        elif ret < - 180:
            ret = 180 + ret
        if ret > 90:
            ret = 180 - ret
        elif ret < -90:
            ret = -180 - ret
        return ret

    return adjustOverFlow(ret)
    

#在某个确定的点，顺次沿东西, 和南北 各平移一定距离得到的新坐标点
#按照坐标表示惯例，东正西负，南正北负
def shiftCoord(lat, lng, distEW, distNS):
    return getLatitudeShift(distEW) + lat, getLongitudeShift(lat, distNS) + lng

    

if __name__ == "__main__":
    #网商路滨安路路口
    #30.186672, 120.192796
    lat,lng = 30.186672, 120.192796
    dist = -0.3
    newLat = getLatitudeShift(dist) + lat
    newLng = getLongitudeShift(lat, dist) + lng
    print (newLat,newLng), getDistHaverisine(lat,lng, newLat,newLng)


