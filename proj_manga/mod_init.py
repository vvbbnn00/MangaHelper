from proj_manga.mod_file import logger_init
from proj_manga.mod_imports import *
from proj_manga.mod_settings import settinginit



def is64windows():
    return 'PROGRAMFILES(X86)' in os.environ


def init():
    print("服务器正在启动")
    settinginit()
    logger_init()

