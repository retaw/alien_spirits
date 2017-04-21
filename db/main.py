# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-12 18:15 +0800
#
# Description: 
#

import __init__
import gevent

class MysqlConnector:
    def connect():
        dbCfgPath = "./config/db_mysql.cfg"
        config = IniParser.IniFile(dbCfgPath)
        
        host = config.get("db", "ip")
        port = config.get("db", "port")
        db = config.get("db", "dbname")
        user = config.get("authorized", "username")
        pwd = config.get("authorized", "password")
        
        conn = MySQLdb.connect(
                host = host,
                port = int(port),
                db = db,
                user = user,
                passwd = pwd
                connect_timeout = 10)
    
        return conn

class MysqlHandler:
    def getItemCollection():
        pass
    def getItem
