import datetime
import os
import time

from proj_manga.mod_settings import get_value, set_value


def logger_init():
    logdir = get_value("Log_Dir")
    try:
        if not os.path.exists(logdir):
            os.mkdir(logdir)
    except Exception as e:
        print(e)

def delfile(path):
    try:
        os.remove(path)
        return 0
    except Exception as e:
        return str(e)


def delfolder(path, fileonly=False):
    ret = 0
    try:
        os.rmdir(os.path.abspath(path))
    except FileNotFoundError as e:
        ret = e
    except OSError as e:
        for i in os.listdir(os.path.abspath(path)):
            if os.path.isfile("%s/%s" % (os.path.abspath(path), i)):
                os.remove("%s/%s" % (os.path.abspath(path), i))
            else:
                delfolder("%s/%s" % (os.path.abspath(path), i))
    except Exception as e:
        return e
    finally:
        if not fileonly:
            if ret == 0:
                os.rmdir(os.path.abspath(path))
        return ret


def RunCleaner():
    now_timestamp = int(time.time())
    last_timestamp = int(get_value("Last_TimeStamp"))
    intevral = int(get_value("Clean_Intevral"))
    if now_timestamp >= last_timestamp + intevral:
        from proj_manga.mod_mysql import SetLogStatus
        from proj_manga.mod_mysql import GetLogSingle
        logdir = get_value("Log_Dir")
        tempdir = get_value("Temp_Dir")
        outdir = get_value("Output_Dir")
        delfolder(tempdir, fileonly=True)
        try:
            set_value("Last_TimeStamp", now_timestamp, change=True)
            for i in os.listdir(logdir):
                log_info = GetLogSingle(i.split(".")[0], "System", True)
                # print(i.split(".")[0])
                if log_info == -1:
                    delfile(os.path.join(logdir, i))
                    pass
                else:
                    time_difference = (datetime.datetime.now() - log_info['time']).total_seconds()
                    # print(time_difference)
                    if time_difference > 24 * 3600:
                        SetLogStatus(log_info['logid'], "outdated")
                        delfile(os.path.join(logdir, i))
                        delfolder(os.path.join(outdir, log_info['logid']))
        except:
            pass

if __name__ == '__main__':
    RunCleaner()