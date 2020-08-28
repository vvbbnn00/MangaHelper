import _thread

from proj_manga.mod_imports import *
from proj_manga.mod_safety import pass_hash, s_passencrypt
from proj_manga.mod_settings import get_value, set_value

Mysql_host = get_value("Mysql_host")
Mysql_pass = get_value("Mysql_pass")
Mysql_db = get_value("Mysql_db")
Mysql_user = get_value("Mysql_user")

temprory_token_list = {}


def initialize():
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


def UpdateUser(username, password, email, s_host, s_pass, chara, s_port, kindleemail):
    # 更新用户
    ori = email
    ori = ori.encode("utf8")
    emailmd5 = hashlib.md5(ori).hexdigest()
    user = GetUser(username)
    if password == "" and user['username'] != None:
        password = GetUser(username)['pass_hash']
    else:
        password = pass_hash(password)
    s_pass = str(s_passencrypt(s_pass), encoding="utf-8")
    db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
    cursor = db.cursor()
    if user['username'] == None:
        sql = """INSERT INTO MANGA_USER(UUID, USERNAME, EMAIL, PASS, KINDLEEMAIL, S_HOST, S_PORT, S_PASS, CHARA, EMAILMD5)
             VALUES (uuid(), '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (
        username, email, password, kindleemail, s_host, s_port, s_pass, chara, emailmd5)
    else:
        uuid = user['uuid']
        sql = """REPLACE INTO MANGA_USER(UUID, USERNAME, EMAIL, PASS, KINDLEEMAIL, S_HOST, S_PORT, S_PASS, CHARA, EMAILMD5)
                     VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (
            uuid, username, email, password, kindleemail, s_host, s_port, s_pass, chara, emailmd5)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return 0
    except Exception as e:
        db.rollback()
        db.close()
        return e


def GetUser(username):
    # 获得用户详细信息
    try:
        db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM MANGA_USER WHERE USERNAME = '%s'" % (username)
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        user = {}
        user['uuid'] = result[0]
        user['username'] = result[1]
        user['email'] = result[2]
        user['pass_hash'] = result[3]
        user['kindle_email'] = result[4]
        user['s_host'] = result[5]
        user['s_port'] = result[6]
        user['s_pass'] = result[7]
        user['authorization'] = result[8]
        user['emailmd5'] = result[9]
        return user
    except:
        user = {}
        user['uuid'] = None
        user['username'] = None
        user['email'] = None
        user['pass_hash'] = None
        user['kindle_email'] = None
        user['s_host'] = None
        user['s_port'] = None
        user['s_pass'] = None
        user['authorization'] = None
        user['emailmd5'] = None
        return user


def CheckUser(username, password):
    # 判断用户名密码是否正确
    try:
        db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM MANGA_USER WHERE USERNAME = '%s'" % (username)
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        passwd = result[3]
        uuid = result[0]
        if pass_hash(password) == passwd:
            token = pass_hash(uuid + username + passwd)
            temprory_token_list[token] = username
            return token
        else:
            return -1
    except:
        return -1


def GetUsername(token):
    # 从token获取用户名
    if temprory_token_list.__contains__(token):
        return temprory_token_list[token]
    else:
        return -1


def CreateTask(url, start, end, all, sendmail, merge, token):
    from proj_manga.mod_dmzjsearch import Analyze_dmzj
    username = GetUsername(token)
    logid = "downlog_" + username + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    if (start == "") or (end == ""):
        downlist = []
    else:
        downlist = range(int(start), int(end) + 1)
    try:
        if all == "true":
            all = True
        elif all == "false":
            all = False
        else:
            return -1
        if sendmail == "true":
            sendmail = True
        elif sendmail == "false":
            sendmail = False
        else:
            return -1
        if merge == "true":
            merge = True
        elif merge == "false":
            merge = False
        else:
            return -1
        db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
        cursor = db.cursor()
        sql = """REPLACE INTO MANGA_DOWNLOAD(USER, LOGID, TIME, STATUS)
                     VALUES ('%s', '%s', '%s', '%s')""" % (
        username, logid, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "queuing")
        cursor.execute(sql)
        db.close()
        _thread.start_new_thread(Analyze_dmzj, (url, "pdf", downlist, all, logid, sendmail, merge, token))
        return logid
    except Exception as e:
        db.close()
        return e

def SetLogStatus(logid, status):
    try:
        db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM MANGA_DOWNLOAD WHERE LOGID = '%s'" % (logid)
        cursor.execute(sql)
        result = cursor.fetchone()
        user = result[0]
        time = result[2]
        sql = """REPLACE INTO MANGA_DOWNLOAD(USER, LOGID, TIME, STATUS)
                     VALUES ('%s', '%s', '%s', '%s')""" % (
            user, logid, time, status)
        cursor.execute(sql)
        db.close()
        return 0
    except:
        return -1

def GetLogSingle(logid, token, fromsystem=False):
    try:
        db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT * FROM MANGA_DOWNLOAD WHERE LOGID = '%s'" % (logid)
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        if result == None:
            return -1
        user = GetUser(GetUsername(token))
        if (result[0] != user['username']) and (user['authorization'] != "管理员") and (not fromsystem):
            return -1
        log = {}
        log['username'] = result[0]
        log['logid'] = result[1]
        log['time'] = result[2]
        log['status'] = result[3]
        return log
    except:
        log = {}
        log['username'] = None
        log['logid'] = None
        log['time'] = None
        log['status'] = None
        return log

def GetLogListFromToken(token):
    # try:
    username = GetUsername(token)
    user = GetUser(username)
    db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
    cursor = db.cursor()
    if user['authorization'] == "管理员":
        sql = "SELECT * FROM MANGA_DOWNLOAD"
    else:
        sql = "SELECT * FROM MANGA_DOWNLOAD WHERE USER = '%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result[::-1]

def GetLog(logid, token, fromsystem=False):
    # try:
    db = MySQLdb.connect(Mysql_host, Mysql_user, Mysql_pass, Mysql_db, charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM MANGA_DOWNLOAD WHERE LOGID = '%s'" % (logid)
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    if result == None:
        return "没有找到这个日记"
    user = GetUser(GetUsername(token))
    if (result[0] != user['username']) and (user['authorization'] != "管理员") and (not fromsystem):
        return "您没有权限访问其他人的日记"
    log = open(get_value('Log_Dir') + logid + ".log", "r")
    text = log.read()
    log.close()
    return text


