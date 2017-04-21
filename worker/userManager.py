# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-14 11:37 +0800
#
# Description: 总的逻辑处理器
#



# userInfo data structer

#allUserInfo =
#{
#    userId1: userInfo1
#    userId2: userInfo2
#    userId3: userInfo3
#    ...
#}


import dbHandler
import geographicalCalc
import itemPicker
import datetime
import random
import logging

logger = logging.getLogger()

db = dbHandler.Mysqlhandler()
itemPicker = itemPicker.ItemPicker()

class UserManager:
    def __init__(self):
        self.openId2UserId = {}
        self.allUserInfo = {}
        pass


    #注册或查找一个openId对应的userId
    def getUserBasicInfo(self, openId):
        def checkOpenId(openId):
            return openId != ""

        if not checkOpenId(openId):
            return 0

        #缓存中没有, 从db中取
        if openId in self.openId2UserId:
            userId = self.openId2UserId[openId]
            userInfo = self.allUserInfo[userId]
            refreshCounter  = userInfo["refresh_counter"]
            powerDeducted   = userInfo["power_deducted"]
            extraPower      = userInfo["extra_power"]
        else:
            (
                userId, 
                uniqueCode, 
                refreshCounter, 
                powerDeducted,
                extraPower,
                playedVideoCodeSet,
                lastRefreshDate,
            ) = db.getBasicUserInfo(openId)

            self.openId2UserId[openId] = userId
            userInfo = {}
            userInfo["userid"] = userId
            userInfo["unique_code"] = uniqueCode
            userInfo["refresh_counter"] = refreshCounter
            userInfo["power_deducted"] = powerDeducted
            userInfo["extra_power"] = extraPower
            userInfo["played_video_code_set"] = playedVideoCodeSet
            userInfo["last_refresh_date"] = lastRefreshDate
            userInfo["items_on_map"] = db.getUserItemsOnMap(userId)
            userInfo["items_captured"] = db.getUserItemsCaptured(userId)
            self.allUserInfo[userId] = userInfo
#            #新用户, 立刻刷新一次地图
#            if refreshCounter == 0:
#                self.refreshUserItemsOnMap(self, userId)
        reverseRefreshTimes = itemPicker.maxTimePerDay - refreshCounter
        avaliablePower = itemPicker.maxPowerPerDay + extraPower - powerDeducted
        logger.info("user login, openId=%s, userId=%d, reverseRefreshTimes=%d, avaliablePower=%d", 
                openId, userId, reverseRefreshTimes, avaliablePower)           
        return userId, avaliablePower, reverseRefreshTimes
    
    def getUserItemsOnMap(self, userId):
        userInfo = self.allUserInfo[userId]
        return userInfo["items_on_map"]

    #每日强制刷新
    def systemForceRefreshUserItemsOnMapToday(self, userId, lat, lng):
        userInfo = self.allUserInfo[userId]
        refreshCounter = userInfo["refresh_counter"]
        powerDeducted = 0
        extraPower = 0
        playedVideoCodeSet = 0
        lastRefreshDate = userInfo["last_refresh_date"]

        now = datetime.datetime.now()
        if lastRefreshDate == now.date():
            return 0, itemPicker.maxTimePerDay - refreshCounter, userInfo["items_on_map"]

        refreshCounter = 0
        itemsOnMap = itemPicker.pickBatchOfItem(lat, lng)
        db.writeUserItemsOnMap(userId, refreshCounter, powerDeducted, extraPower, playedVideoCodeSet, itemsOnMap, now)
        logger.info("[{}], 每日强制刷新成功, auto, itemsOnMap={}".format(userId, itemsOnMap))
        
        userInfo["refresh_counter"] = refreshCounter
        userInfo["power_deducted"] = powerDeducted
        userInfo["extra_power"] = extraPower
        userInfo["played_video_code_set"] = playedVideoCodeSet
        userInfo["items_on_map"] = itemsOnMap
        userInfo["last_refresh_date"] = now.date()
        return 1, itemPicker.maxTimePerDay - refreshCounter, userInfo["items_on_map"]

    #刷新
    def refreshUserItemsOnMap(self, userId, lat, lng):
        userInfo = self.allUserInfo[userId]
        refreshCounter = userInfo["refresh_counter"]
        powerDeducted = userInfo["power_deducted"]
        extraPower = userInfo["extra_power"]
        playedVideoCodeSet = userInfo["played_video_code_set"]
        lastRefreshDate = userInfo["last_refresh_date"]
        if refreshCounter >= itemPicker.maxTimePerDay:
            return 0, itemPicker.maxTimePerDay - refreshCounter, userInfo["items_on_map"]
        now = datetime.datetime.now()
        if lastRefreshDate == now.date():
            refreshCounter += 1
        else:
            refreshCounter = 0
            powerDeducted = 0
            extraPower = 0
            playedVideoCodeSet = 0
        itemsOnMap = itemPicker.pickBatchOfItem(lat, lng)
        now = datetime.datetime.now()
        db.writeUserItemsOnMap(userId, refreshCounter, powerDeducted, extraPower, playedVideoCodeSet, itemsOnMap, now)

        if refreshCounter == 0:
            logger.info("[{}], 每日强制刷新成功, manual, itemsOnMap={}".format(userId, itemsOnMap))
        else:
            logger.info("[{}], 手动刷新成功, refreshCounter={}, itemsOnMap={}".format(userId, refreshCounter, itemsOnMap))
        
        userInfo["refresh_counter"] = refreshCounter
        userInfo["power_deducted"] = powerDeducted
        userInfo["extra_power"] = extraPower
        userInfo["played_video_code_set"] = playedVideoCodeSet
        userInfo["items_on_map"] = itemsOnMap
        userInfo["last_refresh_date"] = now.date()

        return 1, itemPicker.maxTimePerDay - refreshCounter, userInfo["items_on_map"]
        

    #拾取
    def captureItem(self, userId, itemIndex, lat, lng):
        userInfo = self.allUserInfo[userId]

        RET_BAD_QUEST = 0
        RET_SUCCESSFUL = 1
        RET_BAD_LUCK = 2
        RET_NEED_MORE_POWER = 3
        RET_OUT_OF_RANGE = 4

        powerDeducted = userInfo["power_deducted"]
        extraPower = userInfo["extra_power"]
        avaliablePower = itemPicker.maxPowerPerDay + extraPower - powerDeducted

        itemsOnMap = userInfo["items_on_map"]
        if avaliablePower <= 0 :
            return [RET_NEED_MORE_POWER, avaliablePower, itemsOnMap]

        if not (itemIndex in itemsOnMap):
            return [RET_BAD_QUEST, avaliablePower, itemsOnMap]
        
        itemInfo = itemsOnMap[itemIndex]
        itemId  = itemInfo[0]
        itemLat = itemInfo[1]
        itemLng = itemInfo[2]
        
        if not itemPicker.checkCaptureDist(lat, lng, itemLat, itemLng):
            logger.info("[%d], 无法拾取,  距离太远", userId)
            return RET_OUT_OF_RANGE, avaliablePower, {}

        powerDeducted += 1

        badLuck = False
        if random.randint(0, 99) < 5:
            badLuck = True
        
        db.updateItemCatpured(userId, itemId, itemIndex, badLuck, powerDeducted)
        del itemsOnMap[itemIndex]
        userInfo["power_deducted"] = powerDeducted
        avaliablePower = itemPicker.maxPowerPerDay + extraPower - powerDeducted

        if badLuck:
            logger.info("[%d], 拾取失败, badLuck, avaliablePower=%d, itemId=%d, itemIndex=%d", 
                    userId, avaliablePower, itemId, itemIndex)
            return RET_BAD_LUCK, avaliablePower, {}

        itemsCaptured = userInfo["items_captured"]
        if itemId in itemsCaptured:
            itemsCaptured[itemId] = itemsCaptured[itemId] + 1
        else:
            itemsCaptured[itemId] = 1
        logger.info("[%d], 拾取成功, avaliablePower=%d, itemId=%d, itemIndex=%d", 
                userId, avaliablePower, itemId, itemIndex)
        return RET_SUCCESSFUL, avaliablePower, {itemIndex: [itemId, itemLat, itemLng]}


    # 获取userId所拥有的items
    def getUserItemsCaptured(self, userId):
        userInfo = self.allUserInfo[userId]
        return userInfo["items_captured"], userInfo["unique_code"]

    
    #增加userId所对应的
    def addPower(self, userId, actType, videoCode):
        MAX_ACT_TYPE        = 2
        ACT_WATCHED_VIDEO   = 1
        ACT_SHARED          = 2
        POWER_INC_ACT_WATCHED_VIDEO = 1
        POWER_INC_ACT_SHARED = 5
        VIDEO_CODE_SET = (0x01, 0x02, 0x04, 0x08, 0x10)
#        MAX_EXTRA_POWER_INC_BY_WATCH_VIDEO = len(VIDEO_CODE_SET) * POWER_INC_ACT_WATCHED_VIDEO
        MAX_ACCEPTABLE_SHARED_POWER = 3 * POWER_INC_ACT_SHARED

        DEFAULT_POWER_PER_DAY = 30
#        MAX_EXTRA_POWER_DAY = 11

        userInfo = self.allUserInfo[userId]

        powerDeducted = userInfo["power_deducted"]
        extraPower = userInfo["extra_power"]

        #检查actionType的合法性
        if (actType > MAX_ACT_TYPE) or (actType <= 0):
            return 0, itemPicker.maxPowerPerDay + extraPower - powerDeducted, extraPower

        playedVideoCodeSet = userInfo["played_video_code_set"]
        if actType == ACT_WATCHED_VIDEO:
            #检查playedVideoCode合法性, 
            if not videoCode in VIDEO_CODE_SET:
                return 0, itemPicker.maxPowerPerDay + extraPower - powerDeducted, extraPower
            #播放过的不再生效
            if (videoCode & playedVideoCodeSet) != 0:
                logger.info("[%d], addPower 失败, ACT_WATCHED_VIDEO, 视频编号重复, videoCode=%d", userId, videoCode)
                return 0, itemPicker.maxPowerPerDay + extraPower - powerDeducted, extraPower
            playedVideoCodeSet = (playedVideoCodeSet | videoCode)
            extraPower += POWER_INC_ACT_WATCHED_VIDEO
            logger.info("[%d], addPower 失败, ACT_WATCHED_VIDEO, videoCode=%d", userId, videoCode)
        else:
            #看视频增加的power
            extraPowerByWatchVideo = 0
            for vc in VIDEO_CODE_SET:
                if (vc & playedVideoCodeSet) > 0:
                    extraPowerByWatchVideo += 1
            extraPowerByShare =  extraPower - extraPowerByWatchVideo
            if extraPowerByShare >= MAX_ACCEPTABLE_SHARED_POWER:
                logger.info("[%d], addPower 失败, ACT_SHARED, 达到每日分享上限", userId)
                return 0, itemPicker.maxPowerPerDay + extraPower - powerDeducted, extraPower
            extraPower += POWER_INC_ACT_SHARED

        db.updateExtraPower(userId, extraPower, playedVideoCodeSet)
        userInfo["extra_power"] = extraPower
        userInfo["played_video_code_set"] = playedVideoCodeSet
        logger.info("[%d], addPower 成功, videoCode=%d, extraPower=%d", userId, videoCode)
        return 1, itemPicker.maxPowerPerDay + extraPower - powerDeducted, extraPower
        


