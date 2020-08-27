
if __name__ == '__main__':
    import os
    print(os.path.getsize("./log/downlog_admin_20200826160614.log"))
    # init()
    # Analyze_dmzj("http://manhua.dmzj.com/weilenverjidaomowang/", "pdf", [33, 37], False)
    # Analyze_dmzj("https://manhua.dmzj.com/huiyedaxiaojiexiangrangwogaobaitiancaimendelianait/", "pdf",
    #                             [24, 25, 26, 44], False)
    # printerrorlist()

    # Code in mod_init
    # ChromePath = ""
    # print("检测谷歌浏览器是否安装")
    # systemdriv = os.getenv("SystemDrive")
    # if is64windows():
    #     if os.path.exists(systemdriv + "\\Program Files (x86)\\Google\\Chrome\\Application"):
    #         ChromePath = systemdriv + "\\Program Files (x86)\\Google\\Chrome\\Application"
    # else:
    #     if os.path.exists(systemdriv + "\\Program Files\\Google\\Chrome\\Application"):
    #         ChromePath = systemdriv + "\\Program Files\\Google\\Chrome\\Application"
    # if ChromePath == "":
    #     print("没有检测到谷歌浏览器，请安装后再试！")
    #     exit(1)
    # print("检测通过")
    # print("检测ChromeDriver配置")
    # path = pathlib.Path(ChromePath + "/chromedriver.exe")
    # if path.exists():
    #     pass
    #     print("ChromeDriver配置检测通过")
    # else:
    #     print("没有找到ChromeDriver，准备自动安装")
    #     try:
    #         copyfile("./chromedriver.exe", ChromePath + "/chromedriver.exe")
    #     except IOError as e:
    #         print("无法复制文件。" + str(e))
    #         exit(1)
    #     except:
    #         print("未知错误 " + str(sys.exc_info()))
    #         exit(1)
    #     print("安装成功")

    # 暂时弃用
    # class Logger(object):
    #     level_relations = {
    #         'debug': logging.DEBUG,
    #         'info': logging.INFO,
    #         'warning': logging.WARNING,
    #         'error': logging.ERROR,
    #         'crit': logging.CRITICAL
    #     }  # 日志级别关系映射
    #
    #     def __init__(self, filename, level='info', when='D', backCount=3,
    #                  fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
    #         self.logger = logging.getLogger(filename)
    #         format_str = logging.Formatter(fmt)  # 设置日志格式
    #         self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
    #         sh = logging.StreamHandler()  # 往屏幕上输出
    #         sh.setFormatter(format_str)  # 设置屏幕上显示的格式
    #         th = None
    #         if get_value("PrintLog"):
    #             th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
    #                                                    encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
    #         if mod_settings.get_value("PrintLog"):
    #             th.setFormatter(format_str)  # 设置文件里写入的格式
    #             self.logger.addHandler(th)
    #         self.logger.addHandler(sh)  # 把对象加到logger里
    #
    # fmt = "%(asctime)s %(levelname)s %(filename)s %(funcName)s [line:%(lineno)d] %(message)s"
    # datafmt = '%Y-%m-%d %H:%M:%S'
    # handler_1 = logging.StreamHandler()
    # curTime = time.strftime("%Y-%m-%d", time.localtime())  # 获取当前日期
    # handler_2 = RotatingFileHandler(logdir + "/Runtime{0}.log".format(curTime), backupCount=20,
    #                                 encoding='utf-8')
    # # 设置rootlogger 的输出内容形式，输出渠道
    # logging.basicConfig(format=fmt, datefmt=datafmt, level=logging.INFO, handlers=[handler_1, handler_2])
