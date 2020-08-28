from gevent import monkey
# 下面这句不加也能启动服务，但是你会发现Flask还是单线程，在一个请求未返回时，其他请求也会阻塞，所以请添加这句
print("服务器正在启动")
monkey.patch_all()

from proj_manga.mod_imports import *
from proj_manga.mod_init import init
# noinspection PyUnresolvedReferences
from flask import Flask
from proj_manga.mod_safety import randomSecretKey
init()
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
#服务器每次重启都会自动生成新的secret key
app.secret_key = randomSecretKey(64)
app.debug = True


import proj_manga.views
