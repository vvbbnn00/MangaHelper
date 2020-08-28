
def _init():
    global _global_dict
    _global_dict = {}


def settinginit():
    _init()
    set_value("Task_Running", False, local=True)        # （不要更改）任务状态
    set_value("Mysql_host", "localhost", local=True)        # Mysql服务器地址
    set_value("Mysql_user", "operator", local=True)         # Mysql服务器用户名
    set_value("Mysql_pass", "operator", local=True)         # Mysql服务器密码
    set_value("Mysql_db", "db_mangahelper", local=True)     # Mysql数据库名称
    set_value("GenerateBookMark", "True")         # 在生成的PDF中加入书签
    set_value("SearchingEngine", "动漫之家")    # 漫画来源（暂时只有一个动漫之家）
    set_value("CleanOriPDF", "True")              # 在生成完有书签的PDF文件后是否删除原有的PDF（仅适用于GenerateBookMark打开的情况）
    set_value("CleanOriPic", "True")              # 在生成PDF后删除下载的图片
    set_value("Temp_Dir", "temp/")              # 临时文件目录（建议相对路径）
    set_value("Log_Dir", "log/")                # 日志文件目录
    set_value("Output_Dir", "output/")          # 输出文件目录
    set_value("Last_TimeStamp", 0)              # 最后一次清理垃圾的时间
    set_value("Clean_Intevral", 24*3600)        # 清理垃圾的频率（单位：秒）


# 当选项change设定为False时，只会从mysql服务器中获取设置，若在mysql中没有找到设置，则会在mysql中添加默认值，并在_global_dict变量中设置默认值
# 当选项change设定为True时，会将mysql和_global_dict中存储的设置一同更改为指定值
# 当选项local设定为True时，该项设置需要在代码中修改，且此时默认change为True
from proj_manga.mod_imports import *
def set_value(name, value, change=False, local=False):
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
    finally:
       pass
    print(result)

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