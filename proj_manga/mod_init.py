import logging

from proj_manga.mod_file import logger_init
from proj_manga.mod_imports import *
from proj_manga.mod_settings import settinginit

ChromePath = ""


def is64windows():
    return 'PROGRAMFILES(X86)' in os.environ


def init():
    settinginit()
    logger_init()
    ChromePath = ""
    print("检测谷歌浏览器是否安装")
    systemdriv = os.getenv("SystemDrive")
    if is64windows():
        if os.path.exists(systemdriv + "\\Program Files (x86)\\Google\\Chrome\\Application"):
            ChromePath = systemdriv + "\\Program Files (x86)\\Google\\Chrome\\Application"
    else:
        if os.path.exists(systemdriv + "\\Program Files\\Google\\Chrome\\Application"):
            ChromePath = systemdriv + "\\Program Files\\Google\\Chrome\\Application"
    if ChromePath == "":
        print("没有检测到谷歌浏览器，请安装后再试！")
        exit(1)
    print("检测通过")
    print("检测ChromeDriver配置")
    path = pathlib.Path(ChromePath + "/chromedriver.exe")
    if path.exists():
        pass
        print("ChromeDriver配置检测通过")
    else:
        print("没有找到ChromeDriver，准备自动安装")
        try:
            copyfile("./chromedriver.exe", ChromePath + "/chromedriver.exe")
        except IOError as e:
            print("无法复制文件。" + str(e))
            exit(1)
        except:
            print("未知错误 " + str(sys.exc_info()))
            exit(1)
        print("安装成功")
