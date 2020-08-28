import configparser

def _init():
    global _global_dict
    _global_dict = {}

def initialize():
    if not os.path.exists("./installed"):
        fd = open("./installed", mode="w", encoding="utf-8")
        fd.close()
    else:
        return
    Mysql_host = get_value("Mysql_host")
    Mysql_user = get_value("Mysql_user")
    Mysql_pass = get_value("Mysql_pass")
    Mysql_db = get_value("Mysql_db")
    db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
    cursor = db.cursor()
    # 初始化用户信息数据库
    cursor.execute("DROP TABLE IF EXISTS MANGA_USER")
    database = """CREATE TABLE MANGA_USER (
                UUID CHAR (255) NOT NULL PRIMARY KEY ,
                USERNAME CHAR(255) NOT NULL,
                EMAIL CHAR(255),
                PASS CHAR(255) NOT NULL,  
                KINDLEEMAIL CHAR(255), 
                S_HOST CHAR(255), 
                S_PORT CHAR(255), 
                S_PASS CHAR(255),
                CHARA CHAR(255),
                EMAILMD5 CHAR(255)
              )"""
    cursor.execute(database)
    # 初始化下载日志记录数据库
    cursor.execute("DROP TABLE IF EXISTS MANGA_DOWNLOAD")
    database = """CREATE TABLE MANGA_DOWNLOAD (
                USER CHAR(255) NOT NULL,
                LOGID CHAR(255) NOT NULL PRIMARY KEY,
                TIME DATETIME NOT NULL,
                STATUS CHAR(255) NOT NULL
              )"""
    cursor.execute(database)
    cursor.execute("DROP TABLE IF EXISTS MANGA_SETTINGS")
    database = """CREATE TABLE MANGA_SETTINGS (
                SettingName CHAR(255) NOT NULL PRIMARY KEY,
                S_Value CHAR(255) NOT NULL
              )"""
    cursor.execute(database)
    db.close()


def settinginit():
    _init()
    set_value("Task_Running", False, local=True)        # （不要更改）任务状态

    mysqlcfg = "mysql.ini"
    conf = configparser.ConfigParser()
    if not os.path.exists(mysqlcfg):
        f = open(mysqlcfg, 'wb')
        f.close()
    conf.read(mysqlcfg)
    if not conf.has_section("Mysql"):
        conf.add_section("Mysql")

    if not conf.has_option("Mysql", "Mysql_host"):
        conf.set("Mysql", "Mysql_host", "localhost")
        Mysql_host = "localhost"
    else:
        Mysql_host = conf.get("Mysql", "Mysql_host")
    set_value("Mysql_host", Mysql_host, local=True)
    if not conf.has_option("Mysql", "Mysql_user"):
        conf.set("Mysql", "Mysql_user", "root")
        Mysql_user = "root"
    else:
        Mysql_user = conf.get("Mysql", "Mysql_user")
    set_value("Mysql_user", Mysql_user, local=True)
    if not conf.has_option("Mysql", "Mysql_pass"):
        conf.set("Mysql", "Mysql_pass", "root")
        Mysql_pass = "root"
    else:
        Mysql_pass = conf.get("Mysql", "Mysql_pass")
    set_value("Mysql_pass", Mysql_pass, local=True)
    if not conf.has_option("Mysql", "Mysql_db"):
        conf.set("Mysql", "Mysql_db", "db_mangahelper")
        Mysql_db = "db_mangahelper"
    else:
        Mysql_db = conf.get("Mysql", "Mysql_db")
    set_value("Mysql_db", Mysql_db, local=True)
    conf.write(open(mysqlcfg, 'w'))

    initialize()
    result = 0
    result += set_value("GenerateBookMark", "True")         # 在生成的PDF中加入书签
    result += set_value("SearchingEngine", "动漫之家")    # 漫画来源（暂时只有一个动漫之家）
    result += set_value("CleanOriPDF", "True")              # 在生成完有书签的PDF文件后是否删除原有的PDF（仅适用于GenerateBookMark打开的情况）
    result += set_value("CleanOriPic", "True")              # 在生成PDF后删除下载的图片
    result += set_value("Temp_Dir", "temp/")              # 临时文件目录（建议相对路径）
    result += set_value("Log_Dir", "log/")                # 日志文件目录
    result += set_value("Output_Dir", "output/")          # 输出文件目录
    result += set_value("Last_TimeStamp", 0)              # 最后一次清理垃圾的时间
    result += set_value("Clean_Intevral", 24*3600)        # 清理垃圾的频率（单位：秒）
    if result != 0:
        print("错误！请检查您的mysql是否配置正确！")
        exit(1)


# 当选项change设定为False时，只会从mysql服务器中获取设置，若在mysql中没有找到设置，则会在mysql中添加默认值，并在_global_dict变量中设置默认值
# 当选项change设定为True时，会将mysql和_global_dict中存储的设置一同更改为指定值
# 当选项local设定为True时，该项设置需要在代码中修改，且此时默认change为True
from proj_manga.mod_imports import *
def set_value(name, value, change=False, local=False):
    result = None
    if local:
        _global_dict[name] = value
        return
    try:
        db = MySQLdb.connect(_global_dict['Mysql_host'], _global_dict['Mysql_user'], _global_dict['Mysql_pass'],
                             _global_dict['Mysql_db'], charset='utf8')
        cursor = db.cursor()
        database = "SELECT * FROM MANGA_SETTINGS WHERE SettingName = '%s'" % (name)
        cursor.execute(database)
        result = cursor.fetchone()
        if result == None:
            database = """REPLACE INTO MANGA_SETTINGS(SettingName, S_Value)
                         VALUES ('%s', '%s')""" % (name, str(value))
            _global_dict[name] = value
            cursor.execute(database)
        else:
            if change == False:
                _global_dict[name] = result[1]
            else:
                database = """REPLACE INTO MANGA_SETTINGS(SettingName, S_Value)
                             VALUES ('%s', '%s')""" % (name, str(value))
                _global_dict[name] = value
                cursor.execute(database)
        db.close()
    except Exception as e:
        return -1
    return 0
    
def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        print("错误的查询键值 %s" % (name))
        return defValue

# if __name__ == '__main__':
#     settinginit()
#     set_value("GenerateBookMark", "True", change=True)         # 在生成的PDF中加入书签
#     set_value("SearchingEngine", "动漫之家", change=True)    # 漫画来源（暂时只有一个动漫之家）
#     set_value("CleanOriPDF", "True", change=True)              # 在生成完有书签的PDF文件后是否删除原有的PDF（仅适用于GenerateBookMark打开的情况）
#     set_value("CleanOriPic", "True", change=True)              # 在生成PDF后删除下载的图片
#     set_value("Temp_Dir", "temp/", change=True)              # 临时文件目录（建议相对路径）
#     set_value("Log_Dir", "log/", change=True)                # 日志文件目录
#     set_value("Output_Dir", "output/", change=True)          # 输出文件目录
#     set_value("Last_TimeStamp", 0, change=True)              # 最后一次清理垃圾的时间
#     set_value("Clean_Intevral", 24*3600, change=True)        # 清理垃圾的频率（单位：秒）