import IniParser
import MySQLdb



def connectToMySQLdb():
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


if __name__ == "__main__":
    dbConn = connectToMySQLdb()
