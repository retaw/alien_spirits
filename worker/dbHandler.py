# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-13 15:36 +0800
#
# Description: 
#

import IniParser
import sys
import MySQLdb
#import contextlib import closing

import logging
logger = logging.getLogger()

class Mysqlhandler:
    def __init__(self):
        self.__conn = None
        self.connect()

    def connect(self):
#        reload(sys) 
#        sys.setdefaultencoding('utf-8') 

        try:
            cfgPath = "../config/db_mysql.cfg"
            config = IniParser.IniFile(cfgPath)
            
            host = config.get("db", "host")
            port = config.get("db", "port")
            db = config.get("db", "dbname")
            user = config.get("authorized", "username")
            pwd = config.get("authorized", "password")

            print host,port,db,user,pwd
            
            self.__conn = MySQLdb.connect(
                    host = host,
                    port = int(port),
                    db = db,
                    user = user,
                    passwd = pwd,
                    connect_timeout = 10)
        except MySQLdb.Error as e:
            logger.error(e)
            raise
        return

    #########################################
    def getCursor(self):
        try:
            ret = self.__conn.ping()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
        return self.__conn.cursor()

    #########################################
    def commit(self, cursor):
        cursor.close()
        self.__conn.commit()

    #########################################
    def rollback(self, cursor):
        self.__conn.rollback()
        cursor.close()

    #########################################
    #登陆获取用户信息
    def getBasicUserInfo(self, openid):
        cursor = self.getCursor()

        try:
            # step 1: 如果不存在，则插入
            sqlAddUser = "insert into players (openid) select '{}' from (select 1) as a where not exists(select openid from players where openid = '{}') limit 1".format(openid, openid)
            n = cursor.execute(sqlAddUser);
            print "add user, effect: ", n

            # step 2: 如果是新插入，则依据自增列userid的值生成unique_code
            if n > 0:
                sqlSetUniqueCode = "update players set unique_code = fn_userid_to_unique_str(userid), refresh_uts = date(date_sub(now(), interval 1 day)) where openid = '{}'".format(openid)
                n = cursor.execute(sqlSetUniqueCode)

            # setp 3: 查询出新增的数据并返回
            sqlGetUserId = "select userid, unique_code, refresh_counter, power_deducted, extra_power, played_video_code_set, date(refresh_uts) from players where openid = '{}'".format( openid );
            cursor.execute(sqlGetUserId);
            row = cursor.fetchone();
            userid          = row[0]
            unique_code     = row[1]
            refresh_counter = row[2]
            power_deducted  = row[3]
            extra_power     = row[4]
            played_video_code_set = row[5]
            lastRefreshDate = row[6]

            self.commit(cursor)

            return [userid, unique_code, refresh_counter, power_deducted, extra_power, played_video_code_set, lastRefreshDate]
        except MySQLdb.Error as e:
            logger.error(e)
            self.rollback(cursor)
            raise



    #########################################
    def getUserItemsOnMap(self, userId):
        cursor = self.getCursor()
        sqlAddUser = "select item_index, itemid, coord_lat, coord_lng from items_on_map where ownerid = {}".format(userId)
        n = cursor.execute(sqlAddUser)
        ret = {}
        for row in cursor:
            ret[row[0]] = [row[1], row[2], row[3]]
        cursor.close()
        return ret


    #########################################
    def writeUserItemsOnMap(self, userId, refreshCounter, powerDeducted, extraPower, playedVideoCodeSet, itemsOnMap, timestamp):
        cursor = self.getCursor()
        try:
            #step 1: 清理旧的地图物品数据
            sqlClearOldData = "delete from items_on_map where ownerid = {}".format(userId)
            cursor.execute(sqlClearOldData)
            #step 2: 插入新的地图物品数据
            for itemIndex, item in itemsOnMap.iteritems():
                itemId   = item[0]
                coordLat = item[1]
                coordLng = item[2]
                sqlInsertNewItemOnMap = "insert into items_on_map (ownerid, item_index, itemid, coord_lat, coord_lng) values({}, {}, {}, {}, {})".format(userId, itemIndex, itemId, coordLat, coordLng)
                print sqlInsertNewItemOnMap
                cursor.execute(sqlInsertNewItemOnMap)
            #step 3: 更新每日刷新累计次数
            sqlUpdateRefreshCounter = "update players set refresh_counter = {}, power_deducted = {}, extra_power = {}, played_video_code_set = {}, refresh_uts = '{}'  where userid = {}".format(refreshCounter, powerDeducted, extraPower, playedVideoCodeSet, timestamp.isoformat(), userId)
            cursor.execute(sqlUpdateRefreshCounter)

            #step 4: 返回本次刷新的数据库日期
            sqlUpdateRefreshCounter

            #commit
            self.commit(cursor)
        except MySQLdb.Error as e:
            logger.error(e)
            self.rollback(cursor)
            raise
        return

    #########################################
    #保存新捕获的对象, badLuck == True，抓捕失败，从地图删除但是没有得到
    def updateItemCatpured(self, userId, itemId, itemIndex, badLuck, powerDeducted):
        cursor = self.getCursor()

        try:
            #step 1: 删除地图上物品
            sqlDeleteItemOnMap = "delete from items_on_map where item_index = {} and ownerid = {}".format(itemIndex, userId)
            cursor.execute(sqlDeleteItemOnMap)

            #step 2: 增加已获取物品数量
            if not badLuck:
                sqlInsertItemCaptured = "insert into items_captured (ownerid, itemid, num) values({}, {}, 1) on duplicate key update num = num + 1".format(userId, itemId)
                cursor.execute(sqlInsertItemCaptured)

            #step 3: 更新体力消耗值
            sqlUpdatePowerDeducted = "update players set power_deducted = {} where userid = {}".format(powerDeducted, userId)
            cursor.execute(sqlUpdatePowerDeducted)
            #commit 
            self.commit(cursor)
        except MySQLdb.Error as e:
            logger.error(e)
            self.rollback(cursor)
            raise
        return

    #########################################
    def getUserItemsCaptured(self, userId):
        cursor = self.getCursor()

        sqlGetItemsCaptured = "select itemid, num from items_captured where ownerid = {}".format(userId)
        n = cursor.execute(sqlGetItemsCaptured)
        ret = {}
        for row in cursor:
            ret[row[0]] = row[1]
        cursor.close()
        return ret


    ########################################
    def updateExtraPower(self, userId, extraPower, playedVideoCodeSet):
        cursor = self.getCursor()
    
        try:
            sqlUpdatePowerDeducted = "update players set extra_power = {}, played_video_code_set = {} where userid = {}".format(extraPower, playedVideoCodeSet, userId)
            cursor.execute(sqlUpdatePowerDeducted)

            self.commit(cursor)
        except MySQLdb.Error as e:
            logger.error(e)
            self.rollback(cursor)
            raise
        return
        




if __name__ == "__main__":
    hander = Mysqlhandler()
    print hander.getUserId("xaabbccdd")
   
