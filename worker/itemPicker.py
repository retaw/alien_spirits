# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-14 21:49 +0800
#
# Description: 
#



import IniParser
import json
import random
import geographicalCalc

ItemQualityCoe = 1000

class ItemPicker():
    def __init__(self):
        self.maxTimePerDay = 0
        self.numPerBatch = 0
        self.refreshRadius = 0
        self.maxCaptureDist = 0
        self.maxPowerPerDay = 30

        self.itemTypeSizeByQuality = 0
        self.itemDistribution = []

        self.loadCfg()

    def loadCfg(self):
        cfgPath = "../config/game.cfg"
        cfg = IniParser.IniFile(cfgPath)

        self.maxTimePerDay  = int(cfg.get("item_refresh", "max_refresh_times_per_day"))
        self.numPerBatch    = int(cfg.get("item_refresh", "num_per_batch"))
        self.refreshRadius  = float(cfg.get("item_refresh", "refresh_radius"))
        self.maxCaptureDist = float(cfg.get("item_refresh", "max_capture_dist"))

        print cfgPath, self.maxTimePerDay, self.numPerBatch, self.refreshRadius

        itemTypeSizeByQuality   = json.loads(cfg.get("item_refresh", "item_type_size_by_quality"))
        probList                = json.loads(cfg.get("item_refresh", "probability_of_quality"))

        probSum = 0
        self.itemDistribution = []
        for i in range(0, len(probList)):
            probSum += probList[i]
            itemQuality = i + 1

            itemTypeIdList = []
            itemIdQualityBase = itemQuality * ItemQualityCoe
            for j in range(0, itemTypeSizeByQuality[i]):
                itemTypeIdList.append(itemIdQualityBase + j + 1)

            for k in range(0, probList[i]):
                self.itemDistribution.append((itemQuality, itemTypeIdList))


        print self.itemDistribution
        if probSum != 100:
            raise Exception("刷新概率配置错误, 总概率必须等于100", probSum)

    
    def pickBatchOfItem(self, lat, lng):
        ret = {}
        for i in range(0, self.numPerBatch):
            itemQuality, itemTypeIdList = random.choice(self.itemDistribution)
            itemId  = random.choice(itemTypeIdList)
            shiftEW = random.uniform(-self.refreshRadius, self.refreshRadius)
            shiftSN = random.uniform(-self.refreshRadius, self.refreshRadius)
            latAfterShift, lngAfterShift = geographicalCalc.shiftCoord(lat, lng, shiftEW, shiftSN)
            ret[i + 1] = [itemId, latAfterShift, lngAfterShift]
        return ret
        i = 0
        while i < self.numPerBatch:
            shiftEW = random.uniform(-self.refreshRadius, self.refreshRadius)
            shiftSN = random.uniform(-self.refreshRadius, self.refreshRadius)
            latAfterShift, lngAfterShift = geographicalCalc.shiftCoord(lat, lng, shiftEW, shiftSN)
            if geographicalCalc.getDistHaverisine(lat, lng, latAfterShift, lngAfterShift) > self.refreshRadius:
                continue
            itemQuality, itemTypeIdList = random.choice(self.itemDistribution)
            itemId  = random.choice(itemTypeIdList)
            i = i + 1
            ret[i] = [itemId, latAfterShift, lngAfterShift]
        return ret
             
            

    def checkCaptureDist(self, lat0, lng0, lat1, lng1):
        dist = geographicalCalc.getDistHaverisine(lat0, lng0, lat1, lng1)
        return dist <= self.maxCaptureDist


if __name__ == "__main__":
    picker = ItemPicker()
    print picker.pickBatchOfItem(30.186672, 120.192796)

