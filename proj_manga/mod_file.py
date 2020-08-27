from proj_manga.mod_imports import *
from proj_manga.mod_settings import get_value

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


def delfolder(path):
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
        if ret == 0:
            os.rmdir(os.path.abspath(path))
        return ret


