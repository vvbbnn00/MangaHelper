
def _init():
    global _global_dict
    _global_dict = {}


def settinginit():
    _init()
    set_value("GenerateBookMark", True)
    set_value("PrintLog", True)
    set_value("SearchingEngine", "动漫之家")
    set_value("CleanOriPDF", True)
    set_value("CleanOriPic", True)
    set_value("Temp_Dir", "temp/")
    set_value("Log_Dir", "log/")
    set_value("Output_Dir", "output/")
    set_value("Mysql_host", "localhost")
    set_value("Mysql_user", "operator")
    set_value("Mysql_pass", "operator")
    set_value("Mysql_db", "db_mangahelper")


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        print("错误的查询键值 %s" % (name))
        return defValue
